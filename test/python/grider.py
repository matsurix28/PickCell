import tkinter
from tkinter import ttk
import tkinterdnd2 as dnd2

rooot = dnd2.Tk()
rooot.geometry('400x500')
r = ttk.Style()
r.theme_use('classic')
r.configure('MyWidget.TFrame', background='red')
frm1 = ttk.Frame(rooot, style='MyWidget.TFrame', )
#frm1.grid_propagate(0)
frm1.pack(expand=True)
btn = ttk.Button(frm1, text='botan')
btn.grid(row=0, column=0)
#frm2 = ttk.Frame(rooot, style='MyWidget.TFrame')
#frm2.grid(row=0, column=1)
btn2 = ttk.Button(frm1, text='2btn')
btn2.grid(row=1, column=1)
rooot.mainloop()
