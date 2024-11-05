from tkinter import *
from tkinter.ttk import *
from tkinterdnd2 import DND_FILES, TkinterDnD


class WinGUI(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_prompt = self.__tk_prompt(self)
        self.tk_input_input = self.__tk_input_input(self)
        self.tk_qrCode = self.__tk_qrCode(self)
        self.last_content = self.tk_input_input.get(1.0, END).rstrip("\n")

    def __win(self):
        self.title("字符串二维码生成器")
        # 设置窗口大小、居中
        width = 820
        height = 450
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.resizable(width=False, height=False)

    def scrollbar_autohide(self, vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar:
                vbar.lift(widget)
            if hbar:
                hbar.lift(widget)

        def hide():
            if vbar:
                vbar.lower(widget)
            if hbar:
                hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar:
            vbar.bind("<Enter>", lambda e: show())
        if vbar:
            vbar.bind("<Leave>", lambda e: hide())
        if hbar:
            hbar.bind("<Enter>", lambda e: show())
        if hbar:
            hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')

    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')

    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)

    def __tk_prompt(self, parent):
        label = Label(parent, text="输入字符串: ", anchor="center", )
        label.place(x=15, y=15, width=90, height=20)
        return label

    def __tk_input_input(self, parent):
        ipt = Text(parent, undo=True, autoseparators=True, maxundo=-1)
        ipt.place(x=24, y=33, width=380, height=380)
        return ipt

    def __tk_qrCode(self, parent):
        qr_code = Label(parent)
        qr_code.place(x=420, y=33, width=380, height=380)
        return qr_code


class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)

    def __event_bind(self):
        self.tk_input_input.drop_target_register(DND_FILES)
        self.tk_input_input.dnd_bind('<<Drop>>', self.__handle_drop)
        self.tk_input_input.bind('<<Modified>>', self.__start_monitoring)
        pass

    def __style_config(self):
        pass

    def __start_monitoring(self, event=None):
        current_content = self.tk_input_input.get(1.0, END).rstrip("\n")
        byte_length = len(current_content.encode('utf-8'))
        if byte_length > 2048:
            self.tk_qrCode.config(text="字符串太长了")
            self.tk_qrCode.config(image="")
        elif current_content != self.last_content:  # 比较内容是否变化
            self.ctl.generate_qrCode(current_content)
            self.last_content = current_content  # 更新最后内容
        self.after(100, self.__start_monitoring)  # 每100毫秒检查一次

    def __handle_drop(self, event):
        file_path = event.data.strip('{}')
        self.tk_input_input.delete(1.0, END)
        self.tk_input_input.insert(END, file_path)


if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()
