from ui import Win
from tkinter import *
import qrcode


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
        img.show()

        self.ui.tk_button_generate.config(state=NORMAL, text="生成二维码")
        self.ui.isgetdata = False
