import pyvista as pv
from utils.ImageProcessor import ImageProcessor
from utils.ColorAnalyzer import ColorAnalyzer
from tqdm import tqdm
import numpy as np
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class CubeBuilder:
    """
    建模类，用于根据图像生成三维模型，使用优化的体素网格合并。
    """

    def __init__(self, side_length=1, layer_thickness=3):
        """
        :param side_length: 每个立方体的边长，控制生成模型的分辨率和体素大小，默认为 1。
        :param layer_thickness: 每层的厚度，控制图像层的堆叠间隔，默认为 3。
        """
        self.side_length = side_length
        self.layer_thickness = layer_thickness
        self.plotter = pv.Plotter()
        self.color_cubes = {}

    def optimize_mesh(self, mesh):
        """
        优化多边形网格以提高渲染效率。
        """
        # 提取外表面
        surface = mesh.extract_surface()

        # 清理网格
        cleaned = surface.clean()

        # 优化数据类型
        cleaned.points = cleaned.points.astype(np.float32)

        return cleaned

    def generate_surface(self, current_z, image_path):
        """
        根据单张图片生成三维表面，包含优化处理。
        :param current_z: 当前层的高度。
        :param image_path: 图像路径。
        """
        pixels = ImageProcessor.extract_pixel_colors(image_path)


        color_mesh_list = defaultdict(list)

        # 遍历像素并生成立方体
        for x, y, r, g, b, color in pixels:
            if ColorAnalyzer.is_nearly_white(color):
                continue  # 跳过接近白色的像素

            # 直接将立方体存入字典
            color_mesh_list[color].append(
                pv.Cube(
                    center=(x, y, current_z),
                    x_length=self.side_length,
                    y_length=self.side_length,
                    z_length=self.layer_thickness
                )
            )

        # 批量合并并优化
        for color, cubes in color_mesh_list.items():
            # ✅ 合并立方体并优化
            combined_mesh = pv.MultiBlock(cubes).combine()
            optimized_mesh = self.optimize_mesh(combined_mesh)

            # ✅ 直接更新颜色字典（更简洁）
            self.color_cubes[color] = (
                optimized_mesh if color not in self.color_cubes
                else self.color_cubes[color].merge(optimized_mesh)
            )

    def build_model(self, image_paths):
        """
        根据多张图片生成三维模型，使用分层构建方式，并保留颜色信息。
        :param image_paths: 图像路径列表。
        :return: 合并后的完整 PolyData 网格（保留颜色）
        """
        for index, image_path in tqdm(
                enumerate(image_paths), desc="分层建模中", unit="层", total=len(image_paths)
        ):
            current_z = index * self.layer_thickness
            self.generate_surface(current_z=current_z, image_path=image_path)

        # ✅ 合并所有颜色立方体并保留颜色
        all_meshes = []
        all_colors = []

        for color, mesh in self.color_cubes.items():
            # 将颜色转换为RGB数组
            rgba_color = np.array([int(color[i:i + 2], 16) for i in (1, 3, 5)] + [255]) / 255.0
            rgba_array = np.tile(rgba_color, (mesh.n_points, 1))

            # ✅ 将颜色数据附加到 mesh 的 point_data
            mesh.point_data['RGB'] = rgba_array
            mesh.point_data.active_scalars_name = 'RGB'

            # 将处理好的网格和颜色保存
            all_meshes.append(mesh)
            all_colors.append(rgba_color)


        combined_mesh = pv.MultiBlock(all_meshes).combine()
        self.plotter.add_mesh(combined_mesh, scalars="RGB", rgb=True)

        return combined_mesh

    def show_model(self):
        """
        显示生成的三维模型。
        """
        self.plotter.show()
