from ui import Win
from tkinter import *
import qrcode
from PIL import Image
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

    def generate_qrCode(self, string=None):
        # """生成二维码并显示在tk中"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )

        qr.add_data(string)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # 将img转换为可以在tk中显示的img_tk
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')  # 将图片保存到内存中

        img_byte_arr.seek(0)   # 将指针指向开头
        img_pil = Image.open(img_byte_arr)  # 打开内存中的图片
        img_resized = img_pil.resize((380, 380))  # 调整图片大小

        img_byte_arr_resized = BytesIO()  # 新建一个BytesIO对象

        img_resized.save(img_byte_arr_resized, format='PNG')   # 将图片保存到内存中
        img_byte_arr_resized.seek(0)  # 将指针指向开头
        img_tk = PhotoImage(data=img_byte_arr_resized.getvalue())   # 将图片转换为tk的PhotoImage对象

        self.ui.tk_qrCode.config(image=img_tk)  # 显示二维码图片
        self.ui.image = img_tk  # 保存图像引用，防止垃圾回收
