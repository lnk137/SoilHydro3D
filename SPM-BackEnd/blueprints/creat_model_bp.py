from flask import Blueprint, jsonify, request
from utils.Pipeline import Pipeline
import logging
creat_model_bp= Blueprint("creat_model_bp", __name__)
logger=logger = logging.getLogger(__name__)

@creat_model_bp.route("/point_cloud", methods=["POST"])
def point_cloud():
    try:
        # 从前端获取图片文件夹路径
        folder_path = request.json["image_paths"]
        output_path = request.json["output_path"]
        layer_thickness = request.json["layer_thickness"]

        image_paths, temp_folder = Pipeline.preprocess_images(folder_path)
        Pipeline.creat_point_cloud(image_paths, temp_folder, output_path,layer_thickness)

        return jsonify({"status": "点云模型已创建"})

    except Exception as e:
        logger.info(f"点云模型创建失败: {e}")
        return jsonify({"status": f"点云模型创建失败: {e}"})



@creat_model_bp.route("/cube", methods=["POST"])
def cube():
    try:
        # 从前端获取图片文件夹路径
        folder_path = request.json["image_paths"]
        output_path = request.json["output_path"]
        layer_thickness = request.json["layer_thickness"]

        image_paths, temp_folder=Pipeline.preprocess_images(folder_path)
        Pipeline.creat_cube(image_paths, temp_folder, output_path,layer_thickness)

        return jsonify({"status": "立方体模型已创建"})

    except Exception as e:
        logger.info(f"立方体模型创建失败: {e}")
        return jsonify({"status": f"立方体模型创建失败: {e}"})



