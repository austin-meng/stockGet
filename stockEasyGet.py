import tkinter as tk 
from tkinter import filedialog
from tkinter import messagebox
import requests
import os
from datetime import date


class Application(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.addr = tk.StringVar()
        self.code = tk.StringVar()
        self.t0 = tk.StringVar()
        self.t1 = tk.StringVar()

        self.code.set('000001')
        self.t0.set('2016-01-01')
        self.t1.set(str(date.today()))

        self.grid()
     
        self.createWidgets()
        self.createMenu()
        root['menu'] = self.menubar

    def createWidgets(self):
        self.lblCode = tk.Label(self,text="Stock Code:")
        # self.rbShanghai = tk.Radiobutton(self,text='Shanghai',value='sh',variable=self.addr,command=self.changeSH)
        # self.rbShenzhen = tk.Radiobutton(self,text='Shenzhen',value='sz',variable=self.addr,command=self.changeSZ)
        self.lblt0 = tk.Label(self,text="Start Time:")
        self.lblt1 = tk.Label(self,text="End Time:")
        self.lblCode.grid(row=0,column=0,sticky='e')
        self.lblt0.grid(row=1,column=0,sticky='e')
        self.lblt1.grid(row=2,column=0,sticky='e')

        self.entryCode = tk.Entry(self,textvariable=self.code)
        self.entryt0 = tk.Entry(self,textvariable=self.t0)
        self.entryt1 = tk.Entry(self,textvariable=self.t1)
        self.entryCode.grid(row=0,column=1)
        self.entryt0.grid(row=1,column=1)
        self.entryt1.grid(row=2,column=1)

        # self.rbShanghai.grid(row=3,column=0)
        # self.rbShenzhen.grid(row=3,column=1)

        self.btnSavePath = tk.Button(self,text='Save As',command=self.getFilePath)
        self.btnSavePath.grid(row=4,column=0)
        
        self.btnDownload = tk.Button(self,text='Download',command=self.download)
        self.btnDownload.grid(row=4,column=1)

    def createMenu(self):
        self.menubar = tk.Menu(root)
        self.menufile = tk.Menu(self.menubar)
        self.menuhelp = tk.Menu(self.menubar)
        self.menubar.add_cascade(label='File',menu=self.menufile)
        self.menubar.add_cascade(label='Help',menu=self.menuhelp)

        self.menufile.add_command(label='Open',command=self.f_open)
        self.menuhelp.add_command(label='Help',command=self.f_help)
        self.menuhelp.add_separator()
        self.menuhelp.add_command(label='About',command=self.f_about)

    def f_open(self):
        filedialog.askopenfile()

    def f_help(self):
        pass

    def f_about(self):
        pass

    def parseInfo(self):
        t0 = self.t0.get()
        t1 = self.t1.get()
        y_t0, m_t0, d_t0 = t0.split('-')
        y_t1, m_t1, d_t1 = t1.split('-')
        code = self.code.get()
        t0 = t0.replace('-','')
        t1 = t1.replace('-','')
        self.outputpath = t0+'-'+t1+'-'+code+'.txt'
        return (y_t0, int(m_t0)-1, d_t0, y_t1, int(m_t1)-1, d_t1,code,self.outputpath)


    def getFilePath(self):
        self.outputpath = filedialog.asksaveasfilename()

    def download(self):
        url_fmt = "http://table.finance.yahoo.com/table.csv?a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&s=%s"
        code = self.entryCode.get()

        y_t0, m_t0, d_t0, y_t1, m_t1, d_t1,code, self.outputpath= self.parseInfo()

        url = url_fmt % (m_t0, d_t0, y_t0, m_t1, d_t1, y_t1, code+'.ss')
        data = ""
        print(url)
        # exit()
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            data = r.text
            if os.path.exists(self.outputpath):
                print('yes')
                print(self.outputpath)
                os.remove(self.outputpath)
            with open(self.outputpath,'w',encoding='utf-8') as f:
                f.write(data)
            messagebox.showinfo(title='Success',message='Congratulation!\nYou have successfully download stock data!')
        except Exception as e:
            messagebox.showinfo(title='Error',message=e)
            




if __name__ == '__main__':
    root = tk.Tk()
    root.title("Download Stock Data")
    # root.geometry('300x200')
    app = Application(master=root)
    app.mainloop()

