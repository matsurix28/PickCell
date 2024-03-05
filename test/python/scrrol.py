import tkinter as tk
import tkinter.ttk as ttk

txt = 'aa\nb\nc\nd\ne\nf\nf\nhh\nss\n'

root = tk.Tk()
root.geometry('200x100')
frm = ttk.Frame(root, padding=10)
frm.pack(fill='both', expand=True)

cvs = tk.Canvas(frm)
fram = ttk.Frame(cvs)

#frm.grid()
#txt = tk.Text(frm)
scrollbar = ttk.Scrollbar(cvs, orient='vertical', command=cvs.yview)

def resize(event):
    new_w = event.width
    new_h = event.height
    global cvs
    cvs.configure()
    return

scrollbar.pack(side='right', fill='y')
#txt["yscrollcommand"] = scrollbar.set
#txt.grid(row=1, column=0)
#cvs["yscrollcommand"] = scrollbar.set
cvs.configure(scrollregion=(0,0,300,400))
cvs.configure(yscrollcommand=scrollbar.set)
cvs.pack(fill='both', expand=True)

#fram.pack(fill='both', expand=True)

for i in range(20):
    lbl = ttk.Label(fram, text=i)
    lbl.pack()

cvs.create_window((0,0), window=fram, anchor='nw')
#txt.pack()
#scrollbar.grid(row=1, column=1, sticky='NS')
root.mainloop()

