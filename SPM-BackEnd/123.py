from utils.FileManager import FileManager
from utils.PointCloudBuilder import PointCloudBuilder
from utils.ImageProcessor import ImageProcessor
from utils.PyvistaShow import PyvistaShow
from utils.CubeBuilder import CubeBuilder
import logging
import os

# 确保日志目录存在

log_dir = "log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别
    format="[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
    handlers=[
        logging.FileHandler("log/app.log", encoding="utf-8"),  # 将日志输出到文件，设置编码为 utf-8
        logging.StreamHandler()          # 同时输出到控制台
    ]
)
# 获取日志记录器
logger = logging.getLogger(__name__)


# 预处理
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

def creat_point_cloud(image_paths, temp_folder, output_path,layer_thickness,offset=0.3):
    """
    运行点云构建、显示及保存的完整流程。
    """
    try:

        # 初始化点云生成器
        builder = PointCloudBuilder(layer_thickness,offset)
        # 构建点云
        point_cloud=builder.build_point_cloud(image_paths)

        # 保存点云为文件
        FileManager.save_point_cloud_vtp(point_cloud, file_name=output_path)

    finally:
        # 删除 temp 文件夹
        FileManager.delete_temp_folder(temp_folder)
        logger.info("temp 文件夹已删除。")

def creat_cube(image_paths, temp_folder, output_path,layer_thickness=3):
    """
    运行立方体建模、显示及保存的完整流程。
    """
    try:
        builder=CubeBuilder(side_length=1, layer_thickness=layer_thickness)
        # 构建三维模型
        cube_model=builder.build_model(image_paths)
        # 保存为vtk
        FileManager.save_as_vtk(cube_model, output_path)

    finally:
        # 删除 temp 文件夹
        FileManager.delete_temp_folder(temp_folder)
        logger.info("temp 文件夹已删除。")

if __name__ == "__main__":
    # 文件夹路径
    folder_path = r"img/Test/100cut"
    output_path="model/cube.vtk"
    image_paths, temp_folder=preprocess_images(folder_path)


    # 构建点云并显示
    creat_cube(image_paths, temp_folder, output_path=output_path)
    pyvista_show = PyvistaShow()
    pyvista_show.show_mesh_vtk(output_path)
