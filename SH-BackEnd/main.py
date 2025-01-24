import webview
import threading
from flask import Flask, jsonify
from flask_cors import CORS

from blueprints.creat_model_bp import creat_model_bp
from blueprints.file_bp import file_bp
from blueprints.top_bp import top_bp
from blueprints.show_model_bp import show_model_bp

from logging import Filter
import logging
import os


# 确保日志目录存在
log_dir = "backend_log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 清空日志文件内容
log_path = "./backend_log/app.log"
if os.path.exists(log_path):
    with open(log_path, 'w', encoding='utf-8') as f:
        f.truncate()  # 清空文件内容

# 自定义日志过滤器
class APILogFilter(Filter):
    def filter(self, record):
        # 屏蔽对 /get_logs 的访问日志记录
        return "/get_logs" not in record.getMessage()

# 配置日志
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别
    format="[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),  # 将日志输出到文件，设置编码为 utf-8
        logging.StreamHandler()  # 同时输出到控制台
    ]
)

# 获取默认的 Flask werkzeug logger 并添加过滤器
werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.addFilter(APILogFilter())
logger = logging.getLogger(__name__)
app = Flask(__name__)

# 配置跨域请求
CORS(app)

# 注册蓝图
app.register_blueprint(creat_model_bp, url_prefix="/creat")
app.register_blueprint(file_bp, url_prefix="/file")
app.register_blueprint(top_bp, url_prefix="/top")
app.register_blueprint(show_model_bp, url_prefix="/show")


@app.route('/get_logs', methods=['GET'])
def get_logs():
    with open('./backend_log/app.log', 'r', encoding='utf-8') as f:
        logs = f.readlines()
    return jsonify(logs)

def run_flask():
    """ 运行 Flask API 服务器 """
    logger.info("喵喵喵,服务器已启动")
    app.run(host="0.0.0.0", port=4201, debug=True, use_reloader=False)


if __name__ == "__main__":
    try:
        # 创建并启动 Flask 线程
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        webview.DRAG_REGION_SELECTOR = '.top-bar'
        # 启动 WebView 浏览器，访问前端页面
        # webview.create_window("SoilHydro3D", "http://localhost:5173", width=1000, height=800,frameless=True)

        webview.create_window("SoilHydro3D", "web/dist/index.html", width=1000, height=800, frameless=True)
        webview.start(debug=True)

    except Exception as e:
        logger.info(f"服务器启动失败: {e}")
