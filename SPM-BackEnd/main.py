

from utils.ModelBuilder import ModelBuilder
from utils.FileManager import FileManager

if __name__ == "__main__":
    # 文件夹路径
    folder_path = r"img/Test/100"

    # 初始化文件管理器和建模类
    file_manager = FileManager()
    model_builder = ModelBuilder(side_length=1, layer_thickness=3)

    # 加载图片路径
    image_paths = file_manager.load_image_paths_from_folder(folder_path)

    # 构建三维模型
    model_builder.build_model(image_paths)

    # 显示模型
    model_builder.show_model()

    # 保存模型为 PLY 文件
    file_manager.save_colored_model_as_ply(model_builder.plotter, file_name="output_model.ply")

