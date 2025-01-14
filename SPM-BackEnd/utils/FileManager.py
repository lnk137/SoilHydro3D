import os
import shutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
class FileManager:
    """
    文件操作类，用于处理文件的加载和保存。
    """

    @staticmethod
    def load_image_paths_from_folder(folder_path):
        """
        从文件夹中加载所有图片路径。

        :param folder_path: 文件夹路径。
        :type folder_path: str
        :return: 图片路径列表。
        :rtype: List[str]
        """
        image_paths = []
        for filename in os.listdir(folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                img_path = os.path.join(folder_path, filename)
                image_paths.append(img_path)
        return image_paths

    @staticmethod
    def save_point_cloud_vtp(point_cloud, output_path):
        """
        保存点云为 XML 格式的 VTP 文件。

        :param point_cloud: PyVista 的点云数据对象。
        :type point_cloud: pv.PolyData
        :param file_name: 保存的文件名 (.vtp)
        :type file_name: str
        """
        try:
            output_path=FileManager.change_file_extension(output_path, "vtp")
            point_cloud.save(output_path, binary=False)  # binary=False 表示保存为 XML 格式
            logger.info(f"点云已保存为 VTP 格式: {output_path}")
        except Exception as e:
            logger.info(f"保存 VTP 文件时出错: {e}")

    @staticmethod
    def save_as_vtk(mesh, output_path):
        """
        将 PyVista 网格保存为 VTK 文件。
        :param mesh: PyVista 网格对象，必须包含 'RGB' 数据
        :param output_path: 输出 VTK 文件的路径（应以 .vtk 结尾）
        """

        output_path=FileManager.change_file_extension(output_path, "vtk")

        # 检查是否包含 RGB 数据
        if 'RGB' not in mesh.point_data:
            raise ValueError("网格中缺少 RGB 颜色数据")

        # 设置 RGB 为活动标量，用于可视化时显示颜色
        mesh.point_data.active_scalars_name = 'RGB'

        # 保存为 VTK 文件
        mesh.save(output_path)
        logger.info(f"网格已成功保存为 {output_path}")

    @staticmethod
    def save_colored_obj(mesh, output_path):
        pass
        # """
        # 将带有颜色信息的网格保存为 OBJ 格式，并生成相应的 MTL 文件。
        # :param mesh: PyVista 网格对象，必须包含 'RGB' 数据
        # :param output_path: 输出文件路径，将自动添加 .obj 扩展名
        # :raises ValueError: 如果网格中没有颜色数据
        # """
        # # 确保输出路径使用正确的扩展名
        # output_path = str(output_path)
        # if not output_path.lower().endswith('.obj'):
        #     output_path = output_path.rsplit('.', 1)[0] + '.obj'
        #     logger.warning(f"自动将输出文件扩展名修改为 .obj: {output_path}")
        #
        # # 检查颜色数据是否存在
        # if 'RGB' not in mesh.point_data:
        #     raise ValueError("网格中缺少 RGB 颜色数据")
        #
        # try:
        #     # 提取表面网格
        #     surface = mesh.extract_surface()
        #     # 保存为 OBJ 文件，附带颜色信息
        #     surface.save(output_path)
        #     # 获取顶点颜色
        #     colors = mesh.point_data['RGB']
        #     # 用于存储唯一的 RGB 颜色种类
        #     unique_colors = set()
        #
        #     # 用于存储面和材质的对应关系，每个元素为 (面索引, RGB 颜色)
        #     face_material_map = []
        #
        #     # 遍历所有单元
        #     for i in range(mesh.n_cells):
        #         cell = mesh.get_cell(i)
        #         face_indices = cell.point_ids
        #
        #         # 获取该面所有顶点的颜色
        #         face_colors = colors[face_indices]
        #
        #         # 计算平均颜色，只保留 RGB，不包含 Alpha 通道
        #         avg_color = tuple(np.mean(face_colors[:, :3], axis=0))  # 取前三个分量 (R, G, B)
        #
        #         # 将颜色添加到集合中（防止重复）
        #         unique_colors.add(avg_color)
        #
        #         # 将面索引和对应的 RGB 颜色保存到列表中
        #         face_material_map.append((i, avg_color))
        #
        #     # 输出面的数量
        #     print(f"Number of faces: {mesh.n_points}")
        #
        #
        #     # 示例材质映射（可根据 unique_colors 动态生成）
        #     material_map = {
        #         (0.6117, 1.0, 0.6078): "green_material",
        #         (0.0588, 0.9922, 0.996): "cyan_material",
        #         (0.0431, 0.0, 0.9843): "blue_material"
        #     }
        #
        #     with open(output_path, 'r') as input_file, open('../model/color_cube.obj', 'w') as output_file:
        #         lines = input_file.readlines()
        #
        #         # 遍历 face_material_map，根据颜色找到对应材质，并在面上方插入 usemtl
        #         for face_index, color in face_material_map:
        #             material_name = material_map.get(color, "default_material")
        #
        #             # 写入面上方的 usemtl 指令
        #             output_file.write(f"usemtl {material_name}\n")
        #
        #             # 写入对应的面行，face_index + mesh.n_points 定位到正确的面行
        #             output_file.write(lines[face_index + mesh.n_points])
        #
        #
        #     print(f"已成功写入新的 OBJ 文件到 '../model/color_cube.obj'")
        #
        #     logger.info(f"成功保存带颜色的模型到: {output_path}")
        #
        #
        # except Exception as e:
        #     logger.error(f"保存模型文件时发生错误: {str(e)}")
        #     raise

    @staticmethod
    def copy_images_to_temp(source_folder):
        """
        在指定文件夹的子目录中创建 temp 文件夹，并将图片文件复制进去。

        :param source_folder: 源文件夹路径。
        :type source_folder: str
        :return: temp 文件夹的路径。
        :rtype: str
        """
        try:
            # 定义 temp 文件夹路径
            temp_folder = os.path.join(source_folder, "temp")

            # 创建 temp 文件夹
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)
                logger.info(f'创建 temp 文件夹: {temp_folder}')


            # 遍历源文件夹中的所有文件
            for file_name in os.listdir(source_folder):
                file_path = os.path.join(source_folder, file_name)

                # 检查是否为图片文件（支持常见格式）
                if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    # 复制图片文件到 temp 文件夹
                    shutil.copy(file_path, temp_folder)
                    temp_folder = Path(temp_folder).as_posix()

            # 返回 temp 文件夹路径
            return temp_folder

        except Exception as e:
            logger.info(f"复制图片到 temp 文件夹时出错: {e}")
            return None

    @staticmethod
    def delete_temp_folder(temp_folder):
        """
        删除指定目录中的 temp 文件夹及其内容。

        :param source_folder: 源文件夹路径。
        :type source_folder: str
        """
        try:
            # # 定义 temp 文件夹路径
            # temp_folder = os.path.join(source_folder, "temp")
            logger.debug(f"尝试删除文件夹: {temp_folder}")
            # 检查 temp 文件夹是否存在
            if os.path.exists(temp_folder) and os.path.isdir(temp_folder):

                # 删除 temp 文件夹及其内容
                shutil.rmtree(temp_folder)


        except Exception as e:
            logger.info(f"删除 temp 文件夹时出错: {e}")

    @staticmethod
    def change_file_extension(output_path, new_extension):
        """
        修改文件后缀为指定格式
        :param output_path: 原始文件路径 (如 "model/cube.vtk")
        :param new_extension: 目标格式 (如 "obj", "stl", "ply")
        :return: 修改后的新文件路径
        """
        base_name, _ = os.path.splitext(output_path)  # 获取不带后缀的文件名
        new_file_path = f"{base_name}.{new_extension}"  # 拼接新后缀
        return new_file_path