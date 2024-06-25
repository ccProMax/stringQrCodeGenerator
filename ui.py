from tkinter import *
from tkinter.ttk import *
import threading


class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_prompt = self.__tk_prompt(self)
        self.tk_input_input = self.__tk_input_input(self)
        self.tk_button_generate = self.__tk_button_generate(self)
        self.isgetdata = False

    def __win(self):
        self.title("字符串二维码生成器")
        # 设置窗口大小、居中
        width = 645
        height = 562
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
        ipt.place(x=24, y=33, width=600, height=450)
        return ipt

    def __tk_button_generate(self, parent):
        btn = Button(parent, text="生成二维码", takefocus=False,)
        btn.place(x=245, y=500, width=150, height=40)
        return btn


class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)

    def __event_bind(self):
        self.tk_button_generate.bind('<Button-1>', self.__start_thread)
        pass

    def __style_config(self):
        pass

    def __start_thread(self, event):
        if self.isgetdata:   # 上一个没有关闭
            return
        self.isgetdata = True
        self.tk_button_generate.config(state=DISABLED, text="已生成二维码")
        thread = threading.Thread(target=self.ctl.generate_qrCode)
        thread.start()


if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()
