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
    layer_thickness = int(request.json["layer_thickness"])
    image_paths, temp_folder = Pipeline.preprocess_images(folder_path)

    return folder_path, layer_thickness, output_path,target,image_paths, temp_folder

@creat_model_bp.route("/point_cloud", methods=["POST"])
def point_cloud():
    try:
        folder_path, layer_thickness, output_path,target,image_paths, temp_folder= get_request()

        image_paths, temp_folder = Pipeline.preprocess_images(folder_path)
        Pipeline.creat_point_cloud(image_paths, temp_folder, output_path,target,layer_thickness)

        return jsonify({"status": "点云模型已创建"})

    except Exception as e:
        logger.info(f"点云模型创建失败: {e}")
        return jsonify({"status": f"点云模型创建失败: {e}"})



@creat_model_bp.route("/cube", methods=["POST"])
def cube():
    try:

        folder_path, layer_thickness, output_path,target,image_paths,temp_folder=get_request()
        Pipeline.creat_cube(image_paths, temp_folder, output_path,target,layer_thickness)

        return jsonify({"status": "立方体模型已创建"})

    except Exception as e:
        logger.info(f"立方体模型创建失败: {e}")
        return jsonify({"status": f"立方体模型创建失败: {e}"})



