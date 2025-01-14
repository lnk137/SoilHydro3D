import pyvista as pv
import logging

logger = logging.getLogger(__name__)

class PyvistaShow:
    def __init__(self, window_title="Pyvista Viewer"):
        """
        初始化窗口显示类。
        :param window_title: 窗口标题
        """
        self.plotter = pv.Plotter(title=window_title)

    def show_point_cloud(self, file_name, point_size=5):
        """
        读取 VTK 或 VTP 文件并显示点云。

        :param file_name: VTK 或 VTP 文件的路径。
        :param point_size: 点的大小，用于控制点在显示窗口中的可视化效果。
        """
        try:
            # 读取 VTK 或 VTP 文件
            point_cloud = pv.read(file_name)

            # 可视化点云
            self.plotter.add_mesh(
                point_cloud,
                scalars="RGB",  # 假设点云或网格中有 RGB 属性
                rgb=True,  # 使用 RGB 颜色渲染
                point_size=point_size,  # 设置点大小
                render_points_as_spheres=True,
            )
            self.plotter.show()

        except Exception as e:
            logger.info(f"读取或显示点云时出错: {e}")

    def show_mesh_vtk(self, file_path):
        """
        读取并显示带有 RGB 颜色的 VTK 文件。
        :param file_path: VTK 文件路径
        """
        # 加载 VTK 文件
        mesh = pv.read(file_path)

        # 检查是否包含 RGB 颜色
        if "RGB" in mesh.point_data:  # 假设颜色存储在点数据中，字段名为 'RGB'
            self.plotter.add_mesh(mesh, scalars="RGB", rgb=True)
        else:
            self.plotter.add_mesh(mesh, show_edges=True)

        # 显示窗口
        self.plotter.show()
