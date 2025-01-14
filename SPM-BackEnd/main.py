import webview
import threading
from flask import Flask
from flask_cors import CORS

from blueprints.creat_model_bp import creat_model_bp
from blueprints.file_bp import file_bp
from blueprints.top_bp import top_bp


import logging
import os


# 确保日志目录存在

log_dir = "log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别
    format="[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
    handlers=[
        logging.FileHandler("./log/app.log", encoding="utf-8"),  # 将日志输出到文件，设置编码为 utf-8
        logging.StreamHandler()      # 同时输出到控制台
    ]
)
logger = logging.getLogger(__name__)
app = Flask(__name__)

# 配置跨域请求
CORS(app)

# 注册蓝图
app.register_blueprint(creat_model_bp, url_prefix="/creat")
app.register_blueprint(file_bp, url_prefix="/file")
app.register_blueprint(top_bp, url_prefix="/top")

def run_flask():
    """ 运行 Flask API 服务器 """
    logger.info("服务器已启动")
    app.run(host="0.0.0.0", port=5464, debug=True, use_reloader=False)


if __name__ == "__main__":
    # 创建并启动 Flask 线程
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # 启动 WebView 浏览器，访问前端页面
    webview.create_window("SoilHydro3D", "http://localhost:5000/viewer")
    webview.start()
