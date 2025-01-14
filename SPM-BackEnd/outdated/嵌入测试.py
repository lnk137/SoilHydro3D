import webview
import tkinter as tk
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ✅ 允许跨域访问

# 创建 Flask 服务器
app = Flask(__name__)

@app.route("/data")
def send_data():
    return jsonify({"message": "Hello from Flask + Tkinter"})

# Tkinter 窗口嵌入 Webview
def create_tkinter_gui():
    root = tk.Tk()
    root.title("Tkinter GUI")
    label = tk.Label(root, text="This is a Tkinter Window inside Webview!")
    label.pack()
    root.mainloop()

# 使用 PyWebView 启动 Vue 前端
def start_webview():
    webview.create_window('Vue + Tkinter Integration', 'http://localhost:5000')
    webview.start(create_tkinter_gui)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
    start_webview()
