import tkinter as tk 
import requests
from tkinter import filedialog
from tkinter import messagebox
# from tkinter import *
import os


class Application(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.addr = tk.StringVar()
        self.code = tk.StringVar()
        self.t0 = tk.StringVar()
        self.t1 = tk.StringVar()

        self.code.set('600690')
        self.t0.set('20160101')
        self.t1.set('20170317')
        self.outputpath = 'stockdata.txt'

        self.grid()
        self.createWidgets()

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

        self.btnSavePath = tk.Button(self,text='Save Path',command=self.getFilePath)
        self.btnSavePath.grid(row=4,column=0)
        
        self.btnDownload = tk.Button(self,text='Download',command=self.download)
        self.btnDownload.grid(row=4,column=1)

    # def changeSH(self):
    #     self.addr.set('sh')
    
    # def changeSZ(self):
    #     self.addr.set('sz')

    def parseDates(self):
        m_t0, d_t0, y_t0 = self.t0.get()


    def getFilePath(self):
        self.outputpath = filedialog.asksaveasfilename()

    def download(self):
        url_fmt = "http://table.finance.yahoo.com/table.csv?a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&s=%s"
        code = self.entryCode.get()
        t0, t1 = self.parseDates()
        url = url_fmt % (0,1,2016,2,17,2017,self.code.get()+'.ss')
        data = ""
        print(url)
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            data = r.text
            if os.path.exists(self.outputpath):
                os.remove(self.outputpath)
            with open(self.outputpath,'w',encoding='utf-8') as f:
                f.write(data)
        except Exception as e:
            messagebox.showinfo(title='Error',message=e)

        # except:
        #     messagebox.showinfo(title='Error',message='Failed to download stock data!')
        if len(data)>0:
            messagebox.showinfo(title='Success',message='Congratulation!\nYou have successfully download stock data!')



if __name__ == '__main__':
    root = tk.Tk()
    root.title("Download Stock Data")
    # root.geometry('300x200')
    app = Application(master=root)
    app.mainloop()

