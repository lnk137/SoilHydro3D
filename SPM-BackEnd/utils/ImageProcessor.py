from PIL import Image
import numpy as np
import cv2
import os
import logging

logger = logging.getLogger(__name__)
class ImageProcessor:

    @staticmethod
    def extract_pixel_colors(image_path):
        """
        使用 OpenCV 提取图片中每个像素的 RGB 和十六进制颜色值。

        :param image_path: 图片的文件路径。
        :type image_path: str
        :return: 每个元素是一个包含像素坐标 (x, y)、RGB 值 (r, g, b) 和十六进制颜色值的元组。
        :rtype: List[Tuple[int, int, int, int, int, str]]
        :raises FileNotFoundError: 如果图片路径无效或图片无法加载。
        :raises ValueError: 如果图片的通道数少于 3（非 BGR 格式）。
        """
        # 加载图片
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)

        # 确保图片加载成功
        if img is None:
            raise FileNotFoundError(f"Image not found or cannot be read: {image_path}")

        # 获取图片的尺寸
        height, width, channels = img.shape
        if channels < 3:
            raise ValueError(f"Image must have at least 3 channels (BGR): {image_path}")

        # 创建一个空列表来存储每个像素的颜色
        pixel_data = []

        # 遍历每个像素
        for x in range(height):
            for y in range(width):
                # 提取像素的 BGR 值，并转换为 RGB
                b, g, r = img[x, y]
                hex_color = f"#{r:02x}{g:02x}{b:02x}"

                # 保存坐标、RGB 和十六进制值
                pixel_data.append((x, y, r, g, b, hex_color))

        return pixel_data

    @staticmethod
    def replace_top_two_rows(image_paths, hex_color='#0B00FB'):
        """
        将图片路径列表中每张图片的最上面两行像素替换成指定的 16 进制颜色值，并直接覆盖原图片。

        :param image_paths: 图片路径列表。
        :type image_paths: List[str]
        :param hex_color: 指定的 16 进制颜色值（如 "#FF5733"）。
        :type hex_color: str
        """
        # 将 16 进制颜色转换为 RGB
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        new_color = (r, g, b)

        for image_path in image_paths:
            try:
                # 打开图片
                image = Image.open(image_path)
                image = image.convert("RGB")  # 确保图片是 RGB 模式

                # 获取图片宽度和高度
                width, height = image.size

                # 修改最上面两行像素
                pixels = image.load()
                for y in range(2):  # 遍历前两行
                    for x in range(width):
                        pixels[x, y] = new_color

                # 保存修改后的图片（覆盖原图片）
                image.save(image_path)

            except Exception as e:
                logger.info(f"Error来自replace_top_two_rows: {e}")

    @staticmethod
    def cluster_images_to_colors(input_folder, hex_colors= ["#9CFF9B", "#0FFDFE", "#0B00FB", "#FFFFFF"]):
        """
        将文件夹中的图片聚类为指定的目标颜色，并直接替换原始图片。

        :param input_folder: 包含待处理图片的文件夹路径。
        :type input_folder: str
        :param hex_colors: 目标颜色的16进制列表。
        :type hex_colors: list[str]
        """
        # 将16进制颜色转换为RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip("#")
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        # 转换所有目标颜色为RGB
        target_colors = {hex_color: hex_to_rgb(hex_color) for hex_color in hex_colors}

        def closest_color(color, target_colors):
            """
            找到与给定颜色最接近的目标颜色。

            :param color: 输入的 RGB 颜色 (r, g, b)。
            :param target_colors: 目标颜色字典，键为颜色名，值为 RGB 值。
            :return: 最接近的目标颜色名。
            """
            color = np.array(color)
            distances = {key: np.linalg.norm(color - np.array(value)) for key, value in target_colors.items()}
            return min(distances, key=distances.get)

        def process_image(image_path, target_colors):
            """
            将图像中的像素聚类到指定的目标颜色，并替换原始图片。

            :param image_path: 输入图像路径。
            :param target_colors: 目标颜色字典，键为颜色名，值为 RGB 值。
            """
            # 打开图像并转换为 RGB 模式
            image = Image.open(image_path).convert("RGB")
            pixels = np.array(image)
            height, width, _ = pixels.shape

            # 将每个像素点聚类到目标颜色
            clustered_pixels = np.zeros_like(pixels)
            for i in range(height):
                for j in range(width):
                    clustered_pixels[i, j] = target_colors[closest_color(pixels[i, j], target_colors)]

            # 替换原图
            clustered_image = Image.fromarray(np.uint8(clustered_pixels))
            clustered_image.save(image_path)

        # 遍历文件夹中的所有图片
        for filename in os.listdir(input_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                image_path = os.path.join(input_folder, filename)
                process_image(image_path, target_colors)

if __name__ == "__main__":
    # 目标颜色的16进制列表
    HEX_COLORS = ["#9CFF9B", "#0FFDFE", "#0B00FB", "#FFFFFF"]

    input_folder = "../img/Four-Color Cluster Images (Original Colors)"  # 输入文件夹路径

