import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry('300x400')
img = Image.open('test/output/daen/1.png')
img = img.resize((48,48))
img = ImageTk.PhotoImage(img)
lb = ttk.Label(root, text='hello', image=img, background='blue', compound='left')
lb.pack(expand=True, fill='both')
root.mainloop()