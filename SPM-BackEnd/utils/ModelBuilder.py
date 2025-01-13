import pyvista as pv
from utils.ImageProcessor import ImageProcessor
from utils.ColorAnalyzer import ColorAnalyzer
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)

class ModelBuilder:
    """
    建模类，用于根据图像生成三维模型。
    """

    def __init__(self, side_length=1, layer_thickness=3):
        """
        :param side_length: 每个立方体的边长，控制生成模型的分辨率和体素大小，默认为 1。
        :type side_length: int

        :param layer_thickness: 每层的厚度，控制图像层的堆叠间隔，默认为 3。
        :type layer_thickness: int

        :param side_length: 每个立方体的边长，决定体素的大小。
        :type side_length: int

        :param layer_thickness: 每层的厚度，决定相邻图像在模型中的高度间隔。
        :type layer_thickness: int

        :param plotter: PyVista 的渲染器对象，用于渲染三维模型。
        :type plotter: pv.Plotter

        :param color_cubes: 存储每种颜色对应的合并网格的字典,键为颜色值 (Hex 字符串)，值为合并后的网格对象。
        :type color_cubes: Dict[str, pv.PolyData]
        """
        self.side_length = side_length
        self.layer_thickness = layer_thickness
        self.plotter = pv.Plotter()
        self.color_cubes = {}

    def generate_surface(self, current_z, image_path):
        """
        根据单张图片生成三维表面。

        :param current_z: 当前层的高度。
        :type current_z: int
        :param image_path: 图像路径。
        :type image_path: str
        """
        pixels = ImageProcessor.extract_pixel_colors(image_path)

        # 用于延迟合并的临时存储字典
        color_mesh_list = {}

        for pixel in tqdm(pixels, desc="像素分组", unit="个", position=1, leave=False):
            color = pixel[5]  # Hex颜色值
            if ColorAnalyzer.is_nearly_white(color):
                continue  # 跳过接近白色的像素

            # 为每个像素生成对应的立方体
            cube = pv.Cube(
                center=(pixel[0], pixel[1], current_z),
                x_length=self.side_length,
                y_length=self.side_length,
                z_length=self.layer_thickness,
            )

            # 延迟合并：将立方体存储到对应颜色的列表中
            if color not in color_mesh_list:
                color_mesh_list[color] = [cube]
            else:
                color_mesh_list[color].append(cube)

        # 批量合并每种颜色的立方体网格
        for color, cubes in color_mesh_list.items():
            combined_mesh = pv.MultiBlock(cubes).combine()  # 合并多个网格
            if color not in self.color_cubes:
                self.color_cubes[color] = combined_mesh
            else:
                self.color_cubes[color] = self.color_cubes[color].merge(combined_mesh)

    def build_model(self, image_paths):
        """
        根据多张图片生成三维模型。

        :param image_paths: 图像路径列表。
        :type image_paths: List[str]
        """
        for index, image_path in tqdm(
            enumerate(image_paths), desc="分层建模中", unit="层", total=len(image_paths), position=0
        ):
            current_z = index * self.layer_thickness
            self.generate_surface(current_z=current_z, image_path=image_path)

        for color, combined_mesh in tqdm(
            self.color_cubes.items(), desc="添加到渲染器", unit="体素", position=2, leave=False
        ):
            self.plotter.add_mesh(combined_mesh, color=color)

    def show_model(self):
        """
        显示生成的三维模型。
        """
        self.plotter.show()
