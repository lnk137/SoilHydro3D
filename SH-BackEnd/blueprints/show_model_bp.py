from flask import Blueprint, jsonify, request
from utils.FileManager import FileManager
from utils.PyvistaShow import PyvistaShow
import logging
show_model_bp= Blueprint("show_model_bp", __name__)
logger = logging.getLogger(__name__)

@show_model_bp.route("/all", methods=["POST"])
def show_point_cloud():
    try:
        logger.info(request.json)
        model_type=request.json["model_type"]

        file_path = FileManager.get_file_path()
        show = PyvistaShow()

        if model_type=="point_cloud":
            show.show_point_cloud(file_path)
        elif model_type=="cube":
            show.show_mesh_vtk(file_path)
        return jsonify({"status": "模型已显示"})

    except Exception as e:
        logger.info(f"模型显示失败: {e}")
        return jsonify({"status": f"模型显示失败: {e}"})







