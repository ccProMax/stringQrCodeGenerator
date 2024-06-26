from ui import Win
from tkinter import *
import qrcode
import time
import tkinter as tk
from io import BytesIO


class Controller:
    # 导入UI类后，替换以下的 object 类型，将获得 IDE 属性提示功能
    ui: Win

    def init(self, ui):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui
        # TODO 组件初始化 赋值操作

    def generate_qrCode(self, evt=None):
        string = self.ui.tk_input_input.get(1.0, END).rstrip("\n")
        if not string:
            self.ui.tk_button_generate.config(state=DISABLED, text="请输入内容")
            time.sleep(0.5)
            self.ui.tk_button_generate.config(state=NORMAL, text="生成二维码")
            self.ui.isgetdata = False
            return
        print(string)
        """生成二维码并显示在tk中"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(string)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        width, height = img.size  # 获取原始图像的宽度和高度
        # img.save("qrcode.png")  # 保存图片到本地

        # 将img转换为可以在tk中显示的img_tk
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        img_tk = PhotoImage(data=img_byte_arr)

        # window = tk.Toplevel()  # 使用Toplevel创建一个子窗口，避免阻塞主界面
        window = tk.Toplevel(self.ui)  # 确保窗口是self.ui.root的子窗口
        window.title("二维码预览")
        window.geometry(f"{width}x{height}")  # 设置窗口大小为图片大小
        # window.grab_set()  # 设置为模态窗口，阻止与父窗口的交互
        # window.focus_set()  # 确保模态窗口获得焦点

        panel = tk.Label(window, image=img_tk)   # 创建Label，显示图片
        panel.image = img_tk  # 保存图像引用，防止垃圾回收
        panel.pack(side="top", fill="both", expand="yes")  # 让Label填充窗口并随窗口大小变化

        # 绑定窗口的销毁事件到回调函数on_window_close
        self.window = window
        window.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def on_window_close(self):
        # 这里放置窗口关闭时需要执行的代码
        self.ui.tk_button_generate.config(state=NORMAL, text="生成二维码")
        self.ui.isgetdata = False
        self.window.destroy()  # 销毁窗口
