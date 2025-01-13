class ColorAnalyzer:
    """
    颜色分析类，提供判断颜色特性的方法。
    """

    @staticmethod
    def hex_to_rgb(hex_color):
        """
        将十六进制颜色转换为 RGB 值。

        :param hex_color: 十六进制颜色字符串，例如 "#FFFFFF"。
        :type hex_color: str
        :return: RGB 值，分别表示红色、绿色和蓝色。
        :rtype: Tuple[int, int, int]
        :raises ValueError: 如果输入的十六进制颜色格式无效。
        """
        if not hex_color.startswith("#") or len(hex_color) != 7:
            raise ValueError(f"Invalid hex color: {hex_color}")

        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return r, g, b

    @staticmethod
    def is_nearly_white(hex_color, threshold=200):
        """
        判断颜色是否接近白色。

        :param hex_color: 十六进制颜色字符串，例如 "#FFFFFF"。
        :type hex_color: str
        :param threshold: 白色判断阈值，RGB 值需要大于该阈值。
        :type threshold: int
        :return: 如果颜色接近白色，返回 True，否则返回 False。
        :rtype: bool
        """
        r, g, b = ColorAnalyzer.hex_to_rgb(hex_color)
        return r > threshold and g > threshold and b > threshold

    @staticmethod
    def is_color_in_range(hex_color, target_color, tolerance):
        """
        判断颜色是否在目标颜色的范围内。

        :param hex_color: 被判断的十六进制颜色字符串，例如 "#F5F5F5"。
        :type hex_color: str
        :param target_color: 目标十六进制颜色字符串，例如 "#FFFFFF"。
        :type target_color: str
        :param tolerance: 允许的 RGB 偏差范围（0-255）。
        :type tolerance: int
        :return: 如果颜色在目标颜色范围内，返回 True，否则返回 False。
        :rtype: bool
        """
        r1, g1, b1 = ColorAnalyzer.hex_to_rgb(hex_color)
        r2, g2, b2 = ColorAnalyzer.hex_to_rgb(target_color)

        return abs(r1 - r2) <= tolerance and \
               abs(g1 - g2) <= tolerance and \
               abs(b1 - b2) <= tolerance
