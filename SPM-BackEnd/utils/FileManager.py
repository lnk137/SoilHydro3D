import os


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
    def save_colored_model_as_ply(plotter, file_name="output_model.ply"):
        """
        保存三维模型为 PLY 文件（支持颜色）。

        :param plotter: PyVista 的 Plotter 对象。
        :type plotter: pv.Plotter
        :param file_name: 保存的文件名。
        :type file_name: str
        """
        try:
            meshes = plotter.meshes

            # 合并所有网格，同时保留顶点的颜色信息
            final_mesh = meshes[0]
            for mesh in meshes[1:]:
                final_mesh = final_mesh.merge(mesh)

            # 确保网格有颜色数据
            if not final_mesh.point_data.get("RGBA"):
                raise ValueError("未找到颜色数据，无法保存为带颜色的 PLY 文件。")

            # 保存为 PLY 文件
            final_mesh.save(file_name)
            print(f"模型已保存为 {file_name}")
        except Exception as e:
            print(f"保存带颜色的文件时出错: {e}")
