import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter.font import Font
import requests
import os
from datetime import date
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd

class Application(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.grid()
        self.createMenu()
        self.createNotebook()       
        root['menu'] = self.menubar

    def createMenu(self):
        self.menubar = tk.Menu(root)
        self.menufile = tk.Menu(self.menubar)
        self.menuhelp = tk.Menu(self.menubar)

        self.menubar.add_cascade(label='File',menu=self.menufile)
        self.menubar.add_cascade(label='Help',menu=self.menuhelp)

        self.menufile.add_command(label='Open',command=self.f_open)
        self.menufile.add_separator()
        self.menufile.add_command(label='Exit',command=root.destroy)

        self.menuhelp.add_command(label='Help',command=self.h_help)
        self.menuhelp.add_command(label='About',command=self.h_about)

    def createNotebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0,column=0,sticky='e'+'w'+'s'+'n')
        
        self.frmData = tk.Frame(self.notebook)
        # self.frmStlist = tk.Frame(self.notebook)
        self.frmDraw = tk.Frame(self.notebook)

        self.notebook.add(self.frmData,text='Download',padding=3)
        # self.notebook.add(self.frmStlist,text='Stock Code',padding=3)
        self.notebook.add(self.frmDraw,text='Draw',padding=3)

        self.createFrmData()
        # self.createFrmStlist()
        self.createFrmDraw()

    def createFrmData(self):
        # txtFont = Font(family='Microsoft Yahei',size=15)
        self.code = tk.StringVar()
        self.market = tk.StringVar()
        self.t0 = tk.StringVar()
        self.t1 = tk.StringVar()
        self.outpath = tk.StringVar()

        self.code.set('000002')
        self.market.set('Shenzhen')
        self.t0.set('2016-01-01')
        self.t1.set(str(date.today()))

        self.lfDownload = tk.LabelFrame(self.frmData,bd=2,text='Download stock data')
        self.lfDownload.grid(row=0,column=0,padx=30,pady=5,ipadx=10,ipady=5)

        self.lblCode = tk.Label(self.lfDownload,text="Stock Code:")
        self.entryCode = tk.Entry(self.lfDownload,textvariable=self.code)

        self.lblmarket = tk.Label(self.lfDownload,text='Choose Market:')
        self.omMarket = tk.OptionMenu(self.lfDownload,self.market,'Shanghai','Shenzhen')
        # self.omMarket.config(font=txtFont) 

        self.lblt0 = tk.Label(self.lfDownload,text="Start Time:")
        self.entryt0 = tk.Entry(self.lfDownload,textvariable=self.t0)

        self.lblt1 = tk.Label(self.lfDownload,text="End Time:")
        self.entryt1 = tk.Entry(self.lfDownload,textvariable=self.t1)

        self.lblSavePath = tk.Label(self.lfDownload,text='Output Path(Optional):')
        self.entryPath = tk.Entry(self.lfDownload,textvariable=self.outpath)

        self.btnSavePath = tk.Button(self.lfDownload,text='Open',command=self.saveas_path,anchor='center')
        self.btnDownload = tk.Button(self.lfDownload,text='Download',command=self.download,anchor='e')
        
        # self.lblstatus = tk.Label(self.frmData,text='Status:')
        # self.statusbar = tk.Label(self.frmData,text=self.status.get(),bd=1,textvariable=self.status)
        
        self.lblCode.grid(row=0,column=0,sticky='w')
        self.entryCode.grid(row=1,column=0,columnspan=2,sticky=tk.E+tk.W)
        self.lblmarket.grid(row=2,column=0,columnspan=2,sticky='w')
        self.omMarket.grid(row=3,column=0,columnspan=2,sticky='w'+'e')
        self.lblt0.grid(row=4,column=0,sticky='w')
        self.entryt0.grid(row=5,column=0,columnspan=2,sticky='w'+'e')
        self.lblt1.grid(row=6,column=0,sticky='w')
        self.entryt1.grid(row=7,column=0,columnspan=2,sticky='w'+'e')
        self.lblSavePath.grid(row=8,column=0,columnspan=2,sticky='w')
        self.entryPath.grid(row=9,column=0,sticky='w'+'e')
        self.btnSavePath.grid(row=9,column=1,sticky='w'+'e')

        self.btnDownload.grid(row=10,column=1,sticky='e')
       

    # def createFrmStlist(self):
    #     pass

    def createFrmDraw(self):
        self.importPath = tk.StringVar()
        self.style = tk.StringVar()
        self.style.set('ggplot')
        self.figtitle = tk.StringVar()
        self.figtitle.set('stock data')
        self.lbCols = tk.StringVar()

        self.lfDraw = tk.LabelFrame(self.frmDraw,text='Set Parameters')
        self.lfDraw.grid(row=0,column=0,padx=30,pady=5,ipadx=10,ipady=5)

        self.lblImportData = tk.Label(self.lfDraw,text='Import Data:')
        self.entryImportData = tk.Entry(self.lfDraw,textvariable=self.importPath)
        self.btnImportData = tk.Button(self.lfDraw,text='Import Data',command=self.importData)
        self.lblSelectCol = tk.Label(self.lfDraw,text='Select Columns to Draw:')
        self.lbSelectCol = tk.Listbox(self.lfDraw,selectmode=tk.EXTENDED,listvariable=self.lbCols,width=18,height=5)
        self.lblStyle = tk.Label(self.lfDraw,text='Choose Style:')
        self.omStyle = tk.OptionMenu(self.lfDraw,self.style,'classic','ggplot','seaborn','seaborn-notebook','seaborn-paper','bmh','grayscale')
        self.lblTitle = tk.Label(self.lfDraw,text='Figure Title:')
        self.entryTitle = tk.Entry(self.lfDraw,textvariable=self.figtitle)
        self.btnDraw = tk.Button(self.lfDraw,text='Draw',state=tk.DISABLED,command=self.drawData)
        self.btnSaveImg = tk.Button(self.lfDraw,text='Save Image',state=tk.DISABLED,command=self.saveImg)

        self.lblImportData.grid(row=0,column=0,sticky='w')
        self.entryImportData.grid(row=1,column=0)
        self.btnImportData.grid(row=1,column=1)
        self.lblSelectCol.grid(row=2,column=0,sticky='w')
        self.lbSelectCol.grid(row=3,column=0,columnspan=2,sticky='e'+'w')
        self.lblStyle.grid(row=4,column=0,sticky='w')
        self.omStyle.grid(row=5,column=0,columnspan=2,sticky='e'+'w')
        self.lblTitle.grid(row=6,column=0,sticky='w')
        self.entryTitle.grid(row=7,column=0,columnspan=2,sticky='e'+'w')
        # listbox
        self.btnDraw.grid(row=8,column=1,sticky='e',ipadx=19)
        self.btnSaveImg.grid(row=9,column=1,sticky='e')

        # self.fig = Figure(figsize=(6, 5), dpi=100)
        # self.ax = self.fig.add_subplot(111)
        # self.canvas = FigureCanvasTkAgg(self.fig, master=self.lfDraw)
        # self.canvas.show()
        # self.canvas.get_tk_widget().grid(row=2,column=0,columnspan=3)
  
    def saveas_path(self):
        fpath = filedialog.asksaveasfilename(title='Save as',filetypes=[('csv files','.csv')])
        self.outpath.set(fpath)

    def f_open(self):
        filedialog.askopenfilename()

    # def f_exit(self):
    #     root.destroy()

    def h_help(self):
        helpInfo = """
        Input Format:\n
        Stock Code: <code>.sh or <code>.sz
        Time: YYYY-MM-DD
        """
        messagebox.showinfo(title='Help',message=helpInfo)

    def h_about(self):
        msg = "Get stock data easily.\n\nDesigned by Austin.\nVersion: 1.0\n2017/3/20"
        messagebox.showinfo(title='About',message=msg)        

    def parseInfo(self):
        t0 = self.t0.get()
        t1 = self.t1.get()
        y_t0, m_t0, d_t0 = t0.split('-')
        y_t1, m_t1, d_t1 = t1.split('-')
        code = self.code.get()
        t0 = t0.replace('-','')
        t1 = t1.replace('-','')
        if len(self.entryPath.get()) == 0:
            self.outpath = './'+t0+'-'+t1+'-'+code+'.csv'
        market = '.sz'
        if self.market.get() is 'Shanghai':
            market = '.sh'
        code += market
        return (y_t0, int(m_t0)-1, int(d_t0), y_t1, int(m_t1)-1, int(d_t1),code,self.outpath)

    def download(self):
        # self.status.set('downloading stock data...')
        url_fmt = "http://table.finance.yahoo.com/table.csv?a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&s=%s"
        y_t0, m_t0, d_t0, y_t1, m_t1, d_t1,code, self.outpath= self.parseInfo()
        url = url_fmt % (m_t0, d_t0, y_t0, m_t1, d_t1, y_t1, code)
        data = ""
        # print(url)
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            data = r.text
            if os.path.exists(self.outpath):
                os.remove(self.outpath)
            with open(self.outpath,'w',encoding='utf-8') as f:
                f.write(data)
            messagebox.showinfo(title='Success',message='Congratulation!\nYou have successfully download stock data!')
        except Exception as e:
            messagebox.showinfo(title='Error',message=e)
        # self.status.set('')

    def importData(self):
        path = filedialog.askopenfilename(title='Choose data',filetypes=[('csv files','.csv')])
        self.importPath.set(path)
        if len(path)>0:
            try:
                self.stock_df = pd.read_csv(path,sep=',',parse_dates=True,index_col='Date')
                self.btnDraw.config(state=tk.NORMAL)
                self.lbCols.set(tuple(self.stock_df.columns[:4]))
            except Exception as e:
                messagebox.showinfo(title='Error',message=e)

    def drawData(self):
        plt.style.use(self.style.get())
        cols = []
        for i in self.lbSelectCol.curselection():
            cols.append(self.lbSelectCol.get(i))
        self.fig = Figure(figsize=(7, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)

        figureTk = tk.Tk()
        figureTk.resizable(False,False)
        self.canvas = FigureCanvasTkAgg(self.fig, master=figureTk)
        # self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0,column=0)        
        self.stock_df.ix[:,cols].plot(ax=self.ax)        
        self.ax.set_title(self.figtitle.get())
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Price')

        self.btnSaveImg.config(state=tk.NORMAL)

    def saveImg(self):
        outfigpath = filedialog.asksaveasfilename(filetypes=[('Image','.png')])
        self.fig.savefig(outfigpath,dpi=400)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Download Stock Data")
    # root.geometry('320x360')
    root.resizable(False,False)
    app = Application(master=root)
    app.mainloop()

