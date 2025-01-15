from flask import Blueprint, jsonify
import webview

top_bp = Blueprint('top_bp', __name__)

# 获取当前窗口对象
window = None

def get_window():
    global window
    if window is None:
        window = webview.windows[0]
    return window

@top_bp.route('/fullscreen', methods=['POST'])
def toggle_fullscreen():
    window = get_window()
    window.toggle_fullscreen()
    return jsonify({"status": "fullscreen toggled"})

@top_bp.route('/minimize', methods=['POST'])
def minimize_window():
    window = get_window()
    window.minimize()
    return jsonify({"status": "window minimized"})

@top_bp.route('/close', methods=['POST'])
def close_window():
    window = get_window()
    window.destroy()
    return jsonify({"status": "window closed"})
