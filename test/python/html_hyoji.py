import tkinter as tk

from tkhtmlview import HTMLText, RenderHTML
from tkinterweb import HtmlFrame

root = tk.Tk()
root.geometry('800x500')


#html_label = HTMLText(root, html=RenderHTML('fvfm.html'))
#html_label.pack()

frame = HtmlFrame(root)
frame.load_file('/workspace/fvfm.html', decode='utf-8', force=True)
frame.pack()

root.mainloop()