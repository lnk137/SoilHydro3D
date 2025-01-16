from flask import Blueprint, jsonify, request
from utils.Pipeline import Pipeline
import logging
creat_model_bp= Blueprint("creat_model_bp", __name__)
logger = logging.getLogger(__name__)


def get_request():
    logger.info(request.json)
    # 从前端获取图片文件夹路径
    folder_path = request.json["folder_path"]
    output_path = request.json["output_path"]
    target = request.json["target"]
    model_type = request.json["model_type"]
    layer_thickness = int(request.json["layer_thickness"])
    pipline = Pipeline(folder_path=folder_path,output_path=output_path,layer_thickness=layer_thickness, target=target,model_type = model_type)
    pipline.preprocess_images()

    return pipline,output_path

@creat_model_bp.route("/point_cloud", methods=["POST"])
def point_cloud():
    try:
        pipline,output_path= get_request()

        pipline.create_point_cloud()

        return jsonify({"status": "点云模型已创建"})

    except Exception as e:
        logger.info(f"点云模型创建失败: {e}")
        return jsonify({"status": f"点云模型创建失败: {e}"})



@creat_model_bp.route("/cube", methods=["POST"])
def cube():
    try:

        pipline,output_path= get_request()

        pipline.create_cube()

        return jsonify({"status": "立方体模型已创建"})

    except Exception as e:
        logger.info(f"立方体模型创建失败: {e}")
        return jsonify({"status": f"立方体模型创建失败: {e}"})



