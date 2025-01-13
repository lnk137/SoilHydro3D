import pyvista as pv
from utils.ImageProcessor import ImageProcessor
from utils.ColorAnalyzer import ColorAnalyzer
from tqdm import tqdm


class ModelBuilder:
    """
    建模类，用于根据图像生成三维模型。
    """

    def __init__(self, side_length=1, layer_thickness=3):
        """
        初始化建模类。

        :param side_length: 每个立方体的边长。
        :type side_length: int
        :param layer_thickness: 每层的厚度。
        :type layer_thickness: int
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

            # 合并同颜色的立方体
            if color not in self.color_cubes:
                self.color_cubes[color] = cube
            else:
                self.color_cubes[color] = self.color_cubes[color].merge(cube)

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
