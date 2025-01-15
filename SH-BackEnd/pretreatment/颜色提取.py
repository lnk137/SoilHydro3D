import os
from PIL import Image

def hex_to_rgb(hex_color):
    """将16进制颜色代码转换为RGB元组。"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def process_image(image_path, target_rgb, output_folder):
    """处理单张图片，将非目标颜色的像素变为白色，并保存到新文件夹。"""
    with Image.open(image_path) as img:
        img = img.convert("RGBA")
        pixels = img.load()

        for y in range(img.height):
            for x in range(img.width):
                r, g, b, a = pixels[x, y]
                if (r, g, b) != target_rgb:
                    pixels[x, y] = (255, 255, 255, a)  # 将非目标颜色变为白色

        # 构造新文件的路径
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_folder, filename)
        img.save(output_path)  # 保存到新的文件夹

def process_single_image(input_image, output_folder, hex_color):
    """处理单张图片，并保存到新文件夹。"""
    target_rgb = hex_to_rgb(hex_color)

    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 处理图片
    print(f"正在处理图片: {input_image}")
    process_image(input_image, target_rgb, output_folder)
    print("图片处理完成。")

# 使用示例
input_image = "聚类图/6_gb.png"  # 替换为单张图片的路径
output_folder = "img"  # 替换为保存处理后图片的文件夹路径
hex_color = "#476D75"  # 目标颜色的16进制代码，替换为你想要的颜色
process_single_image(input_image, output_folder, hex_color)
