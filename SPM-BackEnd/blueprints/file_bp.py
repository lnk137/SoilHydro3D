from flask import Blueprint, jsonify
from tkinter import filedialog, Tk
from utils.FileManager import FileManager
import logging
logger = logging.getLogger(__name__)
file_bp= Blueprint("file_bp", __name__)

@file_bp.route('/get_folder_path', methods=['GET'])
def folder_path():

    folder_path = FileManager.get_folder_path()

    return jsonify({"folder_path": folder_path})


@file_bp.route('/get_file_path', methods=['GET'])
def file_path():

    file_path = FileManager.get_file_path()

    return jsonify({"file_path": file_path})


