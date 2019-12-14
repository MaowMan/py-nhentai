from tkinter import *
from script.download import download_manager
import tkinter.font as tkFont
from tkinter import messagebox
class gui(object):
    def __init__(self):
        self.setup()
        self.widget()
        self.loop()
    def setup(self):
        self.root=Tk()
        self.root.title("Nhentai下載器")
        self.font=tkFont.Font(family="helvetica",size=20)
        self.codevar=StringVar()
    def widget(self):
        self.label=Label(self.root,text="請輸入神的語言：",font=self.font)
        self.entry=Entry(self.root,textvariable=self.codevar,font=self.font)
        self.button=Button(self.root,text="開始",fg="red",font=self.font,command=self.main)
        self.label.grid(row=0,column=0)
        self.entry.grid(row=0,column=1)
        self.button.grid(row=0,column=2)
    def main(self):
        self.root.withdraw()
        messagebox.showinfo("Nhentai下載器","正在下載{}".format(self.codevar.get()))
        download_manager(self.codevar.get())
        self.root.deiconify()
        self.codevar.set("")
        messagebox.showinfo("Nhentai下載器","下載完成")
    def loop(self):
        self.root.mainloop()