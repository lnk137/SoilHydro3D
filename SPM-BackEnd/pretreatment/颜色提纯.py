import os
import numpy as np
from PIL import Image


# 定义目标颜色及其 RGB 值
TARGET_COLORS = {
    "#9CFF9B": (156, 255, 155),  # 绿色
    "#0FFDFE": (15, 253, 254),  # 青色
    "#0B00FB": (11, 0, 251),    # 蓝色
    "#FFFFFF": (255, 255, 255), # 白色
}

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

def process_image(image_path, output_path, target_colors):
    """
    将图像中的像素聚类到指定的目标颜色。

    :param image_path: 输入图像路径。
    :param output_path: 输出图像路径。
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

    # 保存聚类结果为新图像
    clustered_image = Image.fromarray(np.uint8(clustered_pixels))
    clustered_image.save(output_path)

def process_images_in_folder(folder_path, output_folder):
    """
    处理文件夹中的所有图片，将它们聚类到指定颜色。

    :param folder_path: 包含图像的文件夹路径。
    :param output_folder: 保存聚类图像的文件夹路径。
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历文件夹中的所有图片
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, f"clustered_{filename}")
            process_image(input_path, output_path, TARGET_COLORS)

# 运行脚本
if __name__ == "__main__":
    input_folder = "../img/Four-Color Cluster Images (Original Colors)"  # 替换为您的输入文件夹路径
    output_folder = "./123"  # 替换为您的输出文件夹路径
    process_images_in_folder(input_folder, output_folder)
