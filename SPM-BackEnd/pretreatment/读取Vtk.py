import pyvista as pv

def read_vtk_file(file_name):
    """
    读取 VTK 文件并返回点云对象。

    :param file_name: VTK 文件的路径。
    :type file_name: str
    :return: PyVista 的点云数据对象。
    :rtype: pv.PolyData
    """
    try:
        # 读取 VTK 文件
        point_cloud = pv.read(file_name)
        print(f"成功读取点云文件: {file_name}")
        print(f"点数: {point_cloud.n_points}")
        return point_cloud
    except Exception as e:
        print(f"读取 VTK 文件时出错: {e}")
        return None


def visualize_point_cloud(point_cloud, point_size=5):
    """
    可视化点云数据。

    :param point_cloud: PyVista 的点云数据对象。
    :type point_cloud: pv.PolyData
    :param point_size: 点的大小。
    :type point_size: int
    """
    plotter = pv.Plotter()
    plotter.add_mesh(
        point_cloud,
        scalars="RGB",          # 假设点云中有 RGB 属性
        rgb=True,               # 指定颜色为 RGB 格式
        point_size=point_size,  # 设置点大小
        render_points_as_spheres=True,
    )
    plotter.show()


if __name__ == "__main__":
    # VTK 文件路径
    file_name = "../model/point_cloud.vtk"

    # 读取 VTK 文件
    point_cloud = read_vtk_file(file_name)

    # 如果成功读取，进行可视化
    if point_cloud:
        visualize_point_cloud(point_cloud, point_size=8)
