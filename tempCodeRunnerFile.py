import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

class WinGUI:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("拖放文件示例")
        self.tk_input_input = tk.Text(self.root, height=10, width=50)
        self.tk_input_input.pack(pady=10)
        self.tk_qrCode = tk.Label(self.root, text="")
        self.tk_qrCode.pack(pady=10)

    def __event_bind(self):
        self.tk_input_input.drop_target_register(DND_FILES)
        self.tk_input_input.dnd_bind('<<Drop>>', self.__handle_drop)
        self.tk_input_input.bind('<<Modified>>', self.__start_monitoring)

    def __style_config(self):
        pass

    def __start_monitoring(self, event=None):
        current_content = self.tk_input_input.get(1.0, tk.END).rstrip("\n")
        byte_length = len(current_content.encode('utf-8'))
        if byte_length > 2048:
            self.tk_qrCode.config(text="字符串太长了")
            self.tk_qrCode.config(image="")
        elif current_content != getattr(self, 'last_content', ""):  # 比较内容是否变化
            self.ctl.generate_qrCode(current_content)
            self.last_content = current_content  # 更新最后内容
        self.root.after(100, self.__start_monitoring)  # 每100毫秒检查一次

    def __handle_drop(self, event):
        file_path = event.data.strip('{}')
        self.tk_input_input.delete(1.0, tk.END)
        self.tk_input_input.insert(tk.END, file_path)

class Controller:
    def __init__(self):
        self.win = Win(self)

    def init(self, win):
        win.__event_bind()
        win.__style_config()

    def generate_qrCode(self, content):
        # 这里实现生成二维码的逻辑
        print(f"生成二维码: {content}")

if __name__ == "__main__":
    app = Controller()
    app.win.root.mainloop()