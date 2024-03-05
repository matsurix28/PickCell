import tkinter as tk


def main():
    app = App()
    app.start()

count = 0
#textvar = tk.StringVar()


class App():
    def __init__(self) -> None:
        pass

    def start(self):
        root = tk.Tk()
        root.geometry('1280x720')
        btn = tk.Button(root, text='+1', command=self.click)
        btn.pack()
        self.textvar = tk.StringVar()
        self.textvar.set(0)
        lbl = tk.Label(root, textvariable=self.textvar)
        lbl.pack()
        root.mainloop()

    def click(self):
        global count
        count += 1
        print(count)
        self.textvar.set(count)

if __name__ == '__main__':
    main()