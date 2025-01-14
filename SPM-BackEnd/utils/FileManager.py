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
    def save_point_cloud_vtp(point_cloud, file_name):
        """
        保存点云为 XML 格式的 VTP 文件。

        :param point_cloud: PyVista 的点云数据对象。
        :type point_cloud: pv.PolyData
        :param file_name: 保存的文件名 (.vtp)
        :type file_name: str
        """
        try:

            point_cloud.save(file_name, binary=False)  # binary=False 表示保存为 XML 格式
            logger.info(f"点云已保存为 VTP 格式: {file_name}")
        except Exception as e:
            logger.info(f"保存 VTP 文件时出错: {e}")

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