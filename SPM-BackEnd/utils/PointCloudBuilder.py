import pyvista as pv
import numpy as np
from utils.ImageProcessor import ImageProcessor
from utils.ColorAnalyzer import ColorAnalyzer
from tqdm import tqdm
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)
class PointCloudBuilder:
    """
    点云生成类，用于根据图像生成三维点云。
    """

    def __init__(self, layer_thickness):
        """
        初始化点云生成类。

        :param layer_thickness: 每层的厚度，控制图像层的堆叠间隔。
        :type layer_thickness: int
        """
        self.layer_thickness = layer_thickness  # 每层的厚度
        self.points = []  # 存储所有点的 (x, y, z) 坐标
        self.colors = []  # 存储所有点的颜色 (r, g, b)
        self.plotter = pv.Plotter()  # 负责点云的可视化
        self.volume_data = {}  # 存储每种颜色对应的体积数据

    def generate_layer(self, current_z, image_path):
        """
        根据单张图片生成点云，增加点的密度，在 3x3x3 范围内生成。

        :param current_z: 当前层的高度。
        :type current_z: int
        :param image_path: 图像路径。
        :type image_path: str
        """
        pixels = ImageProcessor.extract_pixel_colors(image_path)

        # 定义 3x3x3 范围内的偏移
        offsets = [-0.3, 0.0, 0.3]

        # for pixel in tqdm(pixels, desc="处理像素", unit="个", position=1, leave=False):
        for pixel in pixels:
            color = pixel[5]  # Hex颜色值
            if ColorAnalyzer.is_nearly_white(color):
                continue  # 跳过接近白色的像素
            elif ColorAnalyzer.is_color_in_range(color, "#0B00FB", 50):
                continue

            # 提取 RGB 值
            r = pixel[2]
            g = pixel[3]
            b = pixel[4]

            # 在 3x3x3 的范围内生成点
            for dx in offsets:
                for dy in offsets:
                    for dz in offsets:
                        self.points.append((pixel[0] + dx, pixel[1] + dy, current_z + dz))
                        self.colors.append((r, g, b))

    def build_point_cloud(self, image_paths):
        """
        根据多张图片生成三维点云。

        :param image_paths: 图像路径列表。
        :type image_paths: List[str]
        """
        for index, image_path in tqdm(
                enumerate(image_paths), desc="生成点云层", unit="层", total=len(image_paths), position=0
        ):
            # 计算当前层的高度坐标
            current_z = index * self.layer_thickness

            # 按照层厚度生成点云
            for i in range(current_z, current_z + self.layer_thickness):
                self.generate_layer(current_z=i, image_path=image_path)

    def calculate_volume(self):
        """
        统计相同颜色的点数，并计算每种颜色的体积。

        每 27 个点视为一个 1x1x1 的立方米体积。
        """
        # 统计每种颜色对应的点数
        color_point_count = defaultdict(int)

        for color in self.colors:
            color_point_count[color] += 1

        # 计算每种颜色的体积
        self.volume_data = {color: count / 27 for color, count in color_point_count.items()}

        # 打印结果
        for color, volume in self.volume_data.items():
            logger.info(f"颜色 {color} 的体积为 {volume:.2f} 立方米。")

        return self.volume_data

    def generate_point_cloud(self):
        """
        生成并返回点云对象。

        :return: PyVista 的点云数据对象。
        :rtype: pv.PolyData
        """
        # 转换点和颜色为 NumPy 数组
        points_array = np.array(self.points)
        colors_array = np.array(self.colors)

        # 确保颜色为浮点数并归一化
        colors_array = np.clip(colors_array / 255.0, 0, 1)

        # 创建点云数据对象
        point_cloud = pv.PolyData(points_array)
        point_cloud["RGB"] = colors_array  # 添加 RGB 属性

        # 验证属性
        if "RGB" not in point_cloud.point_data.keys():
            raise ValueError("点云对象中未找到 RGB 属性，请检查颜色数据处理流程。")
        return point_cloud

    def show_point_cloud(self):
        """
        显示生成的点云。
        """
        # 获取点云数据
        point_cloud = self.generate_point_cloud()

        # 可视化点云
        self.plotter.add_mesh(
            point_cloud,
            scalars="RGB",          # 使用 RGB 属性进行渲染
            rgb=True,               # 指定颜色为 RGB 格式
            point_size=5,           # 设置点大小
            render_points_as_spheres=True,
        )
        self.plotter.show()
