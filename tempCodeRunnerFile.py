from ui import Win
from control import Controller
import os
import sys

if getattr(sys, 'frozen', False):
    # 获取打包后可执行文件所在目录的绝对路径
    exe_path = os.path.dirname(sys.executable)
else:
    # 获取当前脚本文件的绝对路径
    exe_path = os.path.dirname(os.path.abspath(__file__))

app = Win(Controller())

if __name__ == "__main__":
    app.mainloop()
