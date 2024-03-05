import tkinter as tk

import tkinterdnd2 as dnd2


def drop(event):
    print(event)

root = dnd2.Tk()
root.geometry('300x400')
frm = tk.Frame(root)
frm.drop_target_register(dnd2.DND_FILES)
frm.dnd_bind('<<Drop>>', drop)
root.mainloop()