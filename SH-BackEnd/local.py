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
    folder_path = r"img/Four-Color Cluster Images (Adjusted Colors)/100"
    output_path="model/pc"
    layer_thickness=5

    pipline = Pipeline(folder_path=folder_path,output_path=output_path,layer_thickness=layer_thickness, target=None,model_type = "point_cloud")
    pipline.preprocess_images()
    pipline.create_section(5)
    #
    pyvista_show = PyvistaShow()
    pyvista_show.show_point_cloud('E:\AAAAAAAA\FrontBackEndProjects\SoilHydro3D\SH-BackEnd\model\pc_part_5.vtk')
