from utils.CubeBuilder import CubeBuilder
from utils.FileManager import FileManager
from utils.ImageProcessor import ImageProcessor
from utils.PointCloudBuilder import PointCloudBuilder
import logging

logger = logging.getLogger(__name__)

class Pipeline:

    # 预处理
    @staticmethod
    def preprocess_images(folder_path):

        # 创建 temp 文件夹并复制图片
        temp_folder = FileManager.copy_images_to_temp(folder_path)

        # 加载图片路径列表
        image_paths = FileManager.load_image_paths_from_folder(temp_folder)

        # 聚类图片颜色
        ImageProcessor.cluster_images_to_colors(temp_folder)

        # 处理图片（替换最上面两行像素颜色）
        ImageProcessor.replace_top_two_rows(image_paths)

        return image_paths, temp_folder

    @staticmethod
    def creat_point_cloud(image_paths, temp_folder, output_path,target ,layer_thickness=1, offset=0.3):
        """
        运行点云构建、显示及保存的完整流程。
        """
        try:

            # 初始化点云生成器
            builder = PointCloudBuilder(layer_thickness, offset,target)
            # 构建点云
            point_cloud = builder.build_point_cloud(image_paths)

            # 保存点云为文件
            FileManager.save_point_cloud_vtk(point_cloud, output_path)

        finally:
            # 删除 temp 文件夹
            FileManager.delete_temp_folder(temp_folder)
            logger.info("temp 文件夹已删除。")

    @staticmethod
    def creat_cube(image_paths, temp_folder, output_path,target, layer_thickness=1):
        """
        运行立方体建模、显示及保存的完整流程。
        """
        try:
            builder = CubeBuilder(side_length=1, layer_thickness=layer_thickness)
            # 构建三维模型
            cube_model = builder.build_model(image_paths)
            # 保存为vtk
            FileManager.save_as_vtk(cube_model, output_path)

        finally:
            # 删除 temp 文件夹
            FileManager.delete_temp_folder(temp_folder)
            logger.info("temp 文件夹已删除。")
