import tkinter as tk
import tkinter.ttk as ttk

def main():
    gui = Gyui()

class Gyui():
    def __init__(self) -> None:
        root = tk.Tk()
        root.geometry('200x100')
        m = MainFrame(root)
        root.mainloop()

class MainFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.canvas = tk.Canvas(self)
        self.frame = ttk.Frame(self.canvas)
        for i in range(30):
            lbl = ttk.Label(self.frame, text=i)
            lbl.pack()
        self.frame.bind('<Expose>', self.resize)
        scrollbar = ttk.Scrollbar(self.canvas, orient='vertical', command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')
        self.canvas.configure(scrollregion=(0,0,200,200))
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_window((0,0), window=self.frame, anchor='nw')
        self.pack(fill='both', expand=True)
        btn = ttk.Button(self, text='btn', command=self.add)
        btn.pack()

    def resize(self, event):
        w = self.frame.winfo_width()
        h = self.frame.winfo_height()
        a = self.frame.size()
        print(w,h, a)
        self.canvas.configure(scrollregion=(0,0,w,h))

    def add(self):
        for i in range(10):
            lbl = ttk.Label(self.frame, text=i)
            lbl.pack()


if __name__ == '__main__':
    main()