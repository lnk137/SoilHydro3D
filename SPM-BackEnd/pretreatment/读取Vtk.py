from flask import Flask, render_template
import pyvista as pv
import panel as pn

app = Flask(__name__)

def create_point_cloud_visualization():
    """
    使用 PyVista 和 Panel 创建一个可交互的 3D 点云可视化界面。
    """
    # 使用示例数据（也可以改成你的 VTK 文件）
    point_cloud = pv.read("../model/cube.vtk")  # 替换为你的 VTK 文件路径

    # 使用 PyVista 可视化
    plotter = pv.Plotter()
    plotter.add_mesh(
        point_cloud,
        scalars="RGB",
        rgb=True,
        point_size=5,
        render_points_as_spheres=True
    )

    # 通过 Panel 将 PyVista 渲染到 Web
    panel_view = plotter.show(jupyter_backend="panel", return_viewer=True)
    return panel_view


@app.route("/")
def home():
    """
    首页，嵌入 VTK 可视化。
    """
    panel_view = create_point_cloud_visualization()
    # ✅ 使用 Panel 将可视化界面转换为 HTML
    panel_view.save("templates/vtk_viewer.html")
    return render_template("vtk_viewer.html")


if __name__ == "__main__":
    # ✅ 启动 Flask 服务器，访问 http://localhost:5000
    app.run(debug=True, port=5000)
