from detect import Detect
import tkinter as tk
import cv2
from PIL import Image, ImageTk

img = cv2.imread('test/output/daen/1.png')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_pil = Image.fromarray(img_rgb)
print(img_pil.size)



root = tk.Tk()
img_tk = ImageTk.PhotoImage(img_pil)
root.title('title dayo')
root.geometry('800x450')
canvas = tk.Canvas(root, width=img.shape[1], height=img.shape[0])
canvas.pack()

canvas.create_image(0,0, image=img_tk, anchor='nw')
root.mainloop()