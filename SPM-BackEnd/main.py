from utils.FileManager import FileManager
from utils.PointCloudBuilder import PointCloudBuilder
from utils.ImageProcessor import ImageProcessor


def initialize_objects(folder_path, layer_thickness):
    """
    初始化文件管理器、点云生成器，以及处理图片所需的路径和对象。

    :param folder_path: 原始图片文件夹路径。
    :type folder_path: str
    :param layer_thickness: 点云的层厚度。
    :type layer_thickness: int
    :return: 文件管理器对象、点云生成器对象、temp 文件夹路径、图片路径列表。
    :rtype: Tuple[FileManager, PointCloudBuilder, str, List[str]]
    """
    # 初始化文件管理器
    file_manager = FileManager()

    # 创建 temp 文件夹并复制图片
    temp_folder = file_manager.copy_images_to_temp(folder_path)

    # 加载图片路径列表
    image_paths = file_manager.load_image_paths_from_folder(temp_folder)

    # 初始化点云生成器
    builder = PointCloudBuilder(layer_thickness=layer_thickness)

    return file_manager, builder, temp_folder, image_paths


def run_point_cloud_pipeline(file_manager, builder, image_paths, temp_folder, output_path):
    """
    运行点云构建、显示及保存的完整流程。

    :param file_manager: 文件管理器对象。
    :type file_manager: FileManager
    :param builder: 点云生成器对象。
    :type builder: PointCloudBuilder
    :param image_paths: 图片路径列表。
    :type image_paths: List[str]
    :param temp_folder: temp 文件夹路径。
    :type temp_folder: str
    :param output_path: 点云文件的保存路径。
    :type output_path: str
    """
    try:
        # 构建点云
        builder.build_point_cloud(image_paths)

        # 显示点云
        builder.show_point_cloud()

        # 生成点云对象
        point_cloud = builder.generate_point_cloud()

        # 保存点云为文件
        file_manager.save_point_cloud(point_cloud, file_name=output_path)

    finally:
        # 删除 temp 文件夹
        file_manager.delete_temp_folder(temp_folder)
        print(f"已删除临时文件夹: {temp_folder}")

if __name__ == "__main__":
    # 文件夹路径
    folder_path = r"img/Four-Color Cluster Images (Adjusted Colors)/100"

    # 创建必要对象
    file_manager, builder, temp_folder, image_paths = initialize_objects(folder_path, layer_thickness=5)

    # 处理图片（替换最上面两行像素颜色）
    ImageProcessor.replace_top_two_rows(image_paths, '#0B00FB')

    # 构建点云并显示
    run_point_cloud_pipeline(file_manager, builder, image_paths, temp_folder, output_path="model/point_cloud.vtk")
