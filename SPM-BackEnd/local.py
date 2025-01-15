from utils.Pipeline import Pipeline
from utils.PyvistaShow import PyvistaShow

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




if __name__ == "__main__":
    # 文件夹路径
    folder_path = r"img/Test/100"
    output_path="model/pc.vtk"
    layer_thickness=3

    image_paths, temp_folder = Pipeline.preprocess_images(folder_path)
    Pipeline.creat_point_cloud(image_paths, temp_folder, output_path, layer_thickness)

    pyvista_show = PyvistaShow()
    pyvista_show.show_point_cloud(output_path)
