import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinterdnd2 as dnd2
from tkinter import ttk

def main():
    app = Application()

class Application:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title('Color Fv/Fm')
        self.root.geometry('1120x630')
        self.__set_parts()
        self.root.mainloop()

    def __set_parts(self):
        button = ttk.Button(self.root, text='Button', command=lambda: self.select('leaf image'))
        button.pack()

    def __create_tabs(self):
        notebook = ttk.Notebook()

    def select(self, target):
        self.filename = filedialog.askopenfilename(title=f'Select {target}', initialdir='./', filetypes=[('Image file', '*.png;*.JPG;*.jpeg'), ('all files', '*')])
        

if __name__ == '__main__':
    main()