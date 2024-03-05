import tkinter as tk
from tkinter import filedialog


def psu():
    filetypes = ['*.bmp', '*.png', '*.PNG', '*.jpg', '*.JPG', '*.jpeg', '*.tiff']
    path = filedialog.askopenfilename(filetypes=[('Image file', filetypes), ('All file', '*')], )
    print(path)

rooot = tk.Tk()
btn = tk.Button(rooot, text='pusu', command=psu)
btn.pack()
rooot.mainloop()