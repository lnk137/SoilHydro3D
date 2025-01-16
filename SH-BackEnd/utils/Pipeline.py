from utils.CubeBuilder import CubeBuilder
from utils.FileManager import FileManager
from utils.ImageProcessor import ImageProcessor
from utils.PointCloudBuilder import PointCloudBuilder
import logging

logger = logging.getLogger(__name__)

class Pipeline:
    def __init__(self, folder_path,output_path,layer_thickness=1, offset=0.3, target=None, model_type=None):
        """
        初始化 Pipeline 实例。
        """
        self.layer_thickness = layer_thickness
        self.offset = offset
        self.target = target
        self.model_type = model_type
        self.output_path = output_path
        self.folder_path = folder_path
        self.temp_folder = None
        self.image_paths = []



    def preprocess_images(self):
        """
        图片预处理：复制图片到临时文件夹、聚类颜色、处理图片。
        """
        # 创建 temp 文件夹并复制图片
        self.temp_folder = FileManager.copy_images_to_temp(self.folder_path)
        # 加载图片路径列表
        self.image_paths = FileManager.load_image_paths_from_folder(self.temp_folder)
        # 聚类图片颜色
        ImageProcessor.cluster_images_to_colors(self.temp_folder)
        # 替换图片最上面两行像素颜色
        ImageProcessor.replace_top_two_rows(self.image_paths)
        logger.info("图片预处理完成。")

    def create_point_cloud(self):
        """
        点云创建、保存及清理流程。
        """
        try:
            builder = PointCloudBuilder(self.layer_thickness, self.offset, self.target)
            point_cloud = builder.build_point_cloud(self.image_paths)
            FileManager.save_point_cloud_vtk(point_cloud, self.output_path)
            logger.info("点云创建并保存完成。")
        except Exception as e:
            logger.error(f"创建点云时出现异常: {e}")
        finally:
            self._cleanup_temp_folder()

    def create_cube(self):
        """
        立方体建模、保存及清理流程。
        """
        try:
            builder = CubeBuilder(side_length=1, layer_thickness=self.layer_thickness, target=self.target)
            cube_model = builder.build_model(self.image_paths)
            FileManager.save_as_vtk(cube_model, self.output_path)
            logger.info("立方体建模并保存完成。")
        except Exception as e:
            logger.error(f"创建立方体时出现异常: {e}")
        finally:
            self._cleanup_temp_folder()

    def create_section(self, n):
        """
        分段立方体建模流程。
        """
        try:
            ImageProcessor.divide_images_into_folders(self.temp_folder, n)
            for i in range(1, n + 1):
                # 生成分段文件夹路径
                section_folder = f"{self.temp_folder}/temp{i}"
                self.image_paths = FileManager.load_image_paths_from_folder(section_folder)

                if self.model_type=="point_cloud":
                    put_path=f"{self.output_path}_part_{i}"
                    builder = PointCloudBuilder(self.layer_thickness, self.offset, self.target)
                    point_cloud = builder.build_point_cloud(self.image_paths)
                    FileManager.save_point_cloud_vtk(point_cloud, put_path)

                elif self.model_type=="cube":
                    put_path=f"{self.output_path}_part_{i}"
                    builder = CubeBuilder(side_length=1, layer_thickness=self.layer_thickness, target=self.target)
                    cube_model = builder.build_model(self.image_paths)
                    FileManager.save_as_vtk(cube_model, put_path)

                logger.info(f"分段 {i} 建模完成并保存。")

        except Exception as e:
            logger.error(f"Error in create_cube_section: {e}")
        finally:
            self._cleanup_temp_folder()

    def _cleanup_temp_folder(self):
        """
        删除临时文件夹。
        """
        if self.temp_folder:
            FileManager.delete_temp_folder(self.temp_folder)
            logger.info("临时文件夹已删除。")
