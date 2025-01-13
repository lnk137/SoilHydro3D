from PIL import Image
import cv2


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
    def replace_top_two_rows(image_paths, hex_color):
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
                print(f"已修改并覆盖图片: {image_path}")

            except Exception as e:
                print(f"处理图片 {image_path} 时出错: {e}")
