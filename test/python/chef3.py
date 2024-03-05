import tkinter as tk

from cefpython3 import cefpython as cef

root = tk.Tk()
root.geometry('800x450')

class BrowserFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.browser = None
        self.bind('<Configure>', self.on_configure)

    def bro(self):
        window_info = cef.WindowInfo()
        self.browser = cef.CreateBrowserSync(window_info, url='/workspace/fvfm.html')

    def on_configure(self, _):
        if not self.browser:
            self.bro()

b = BrowserFrame(root)
b.pack()
root.mainloop()