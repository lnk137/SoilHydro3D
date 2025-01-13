from PIL import Image


def hex_to_rgb(hex_color):
    """将16进制颜色代码转换为RGB格式"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def replace_colors(image_path, colors_to_replace, new_colors, output_path="output.png"):
    # 打开图片并转换为RGBA模式
    img = Image.open(image_path).convert("RGBA")
    data = img.getdata()

    # 定义新的数据列表
    new_data = []

    # 替换指定的三种颜色
    for item in data:
        # 检查当前像素的颜色是否在要替换的颜色列表中
        if item[:3] in colors_to_replace:
            # 找到要替换的颜色对应的索引
            index = colors_to_replace.index(item[:3])
            # 使用新颜色，保留透明度
            new_data.append(new_colors[index] + (item[3],))
        else:
            # 如果不是目标颜色，保持不变
            new_data.append(item)

    # 将新的数据应用到图片中
    img.putdata(new_data)

    # 保存图片
    img.save(output_path)
    print(f"图片已保存为 {output_path}")


if __name__ == "__main__":
    temp='18'
    # 用户输入图片路径
    image_path = f'聚类图/{temp}.png'

    # 输入三种需要替换的颜色（16进制格式）
    # 浅->深
    hex_colors_to_replace = ['#DEE2E0', '#889C97', '#547878']
    colors_to_replace = [hex_to_rgb(color) for color in hex_colors_to_replace]

    # 输入三种替换后的颜色（16进制格式）
    hex_new_colors = ['#9CFF9B', '#0FFDFE', '#0B00FB']
    new_colors = [hex_to_rgb(color) for color in hex_new_colors]
    # #输入三种需要替换的颜色（16进制格式）
    # hex_colors_to_replace = ['#0B00FB']
    # colors_to_replace = [hex_to_rgb(color) for color in hex_colors_to_replace]
    #
    # # 输入三种替换后的颜色（16进制格式）
    # hex_new_colors = ['#FEFEFE']
    # new_colors = [hex_to_rgb(color) for color in hex_new_colors]
    # 输入输出文件路径
    output_path = f"color_img/{temp}.png"

    # 执行颜色替换
    replace_colors(image_path, colors_to_replace, new_colors, output_path)
