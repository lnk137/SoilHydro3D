from flask import Blueprint, jsonify
from tkinter import filedialog

file_bp= Blueprint("file_bp", __name__)



@file_bp.route('/get_path', methods=['GET'])
def getModelPath():
    file_path = filedialog.askopenfilename()
    print(f"选择的文件路径: {file_path}")

    return jsonify({"file_path": file_path})

