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
from bs4 import BeautifulSoup
import re

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
        self.frmStCode = tk.Frame(self.notebook)
        self.frmDraw = tk.Frame(self.notebook)

        self.notebook.add(self.frmData,text='Download',padding=3)
        self.notebook.add(self.frmStCode,text='Stock Code',padding=3)
        self.notebook.add(self.frmDraw,text='Draw',padding=3)

        self.createFrmData()
        self.createFrmStCode()
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
        self.lfDownload.grid(row=0,column=0,padx=30,pady=10,ipadx=10,ipady=5)

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
       

    def createFrmStCode(self):
        self.codeList = tk.StringVar()
        self.status = tk.StringVar()

        self.lfStCode = tk.LabelFrame(self.frmStCode,text='Get Stock Code List')
        self.lfStCode.grid(row=0,column=0,padx=10,pady=5,ipadx=5,ipady=5)

        self.btnFrmWeb = tk.Button(self.lfStCode,text='Get Code from Web',command=self.getCodeList)
        self.lblor = tk.Label(self.lfStCode,text='or')
        self.btnFrmLoc = tk.Button(self.lfStCode,text='Open Files',command=self.importCode)
        self.txtCodeList = tk.Text(self.lfStCode,width=35,height=25)
        self.btnExport = tk.Button(self.lfStCode,text='Export Stock Code',command=self.exportCode)
        # self.scrbar = tk.Scrollbar(self.txtCodeList,orient=tk.VERTICAL)
        # self.txtCodeList.config(yscrollcommand=self.scrbar.set)
        # self.scrbar.config(command=self.txtCodeList.yview)
        # self.lblstatus = tk.Label(self.lfStCode,textvariable=self.status)

        self.btnFrmWeb.grid(row=0,column=0)
        self.lblor.grid(row=0,column=1,padx=10)
        self.btnFrmLoc.grid(row=0,column=2)
        self.txtCodeList.grid(row=1,column=0,columnspan=3,sticky='w'+'e')
        # self.scrbar.grid(row=0,column=1)
        # self.lblstatus.grid(row=2,column=0,sticky='w')
        self.btnExport.grid(row=2,column=2,sticky='e')


    def createFrmDraw(self):
        self.importPath = tk.StringVar()
        self.style = tk.StringVar()
        self.style.set('ggplot')
        self.figtitle = tk.StringVar()
        self.figtitle.set('stock data')
        self.lbCols = tk.StringVar()

        self.lfDraw = tk.LabelFrame(self.frmDraw,text='Set Parameters')
        self.lfDraw.grid(row=0,column=0,padx=30,pady=10,ipadx=10,ipady=5)

        self.lblImportData = tk.Label(self.lfDraw,text='Import Data:')
        self.entryImportData = tk.Entry(self.lfDraw,textvariable=self.importPath)
        self.btnImportData = tk.Button(self.lfDraw,text='Import Data',command=self.importData)
        self.lblSelectCol = tk.Label(self.lfDraw,text='Select Columns to Draw:')
        self.lbSelectCol = tk.Listbox(self.lfDraw,selectmode=tk.EXTENDED,listvariable=self.lbCols,width=18,height=5)
        self.lblStyle = tk.Label(self.lfDraw,text='Choose Style:')
        self.omStyle = tk.OptionMenu(self.lfDraw,self.style,'classic','ggplot','bmh','grayscale','seaborn','seaborn-notebook','seaborn-paper','seaborn-whitegrid', 'seaborn-muted','seaborn-deep',\
          'seaborn-colorblind', 'seaborn-dark', 'seaborn-white', 'seaborn-talk', 'seaborn-poster',\
            'seaborn-dark-palette', 'seaborn-bright', 'seaborn-ticks', 'seaborn-darkgrid', 'fivethirtyeight')
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
        self.btnDraw.grid(row=8,column=1,sticky='e',ipadx=19)
        self.btnSaveImg.grid(row=9,column=1,sticky='e')

    def saveas_path(self):
        fpath = filedialog.asksaveasfilename(title='Save as',filetypes=[('csv files','.csv')])
        self.outpath.set(fpath)

    def f_open(self):
        filedialog.askopenfilename()

    def h_help(self):
        helpInfo = """
        Input Format:\n
        Stock Code: <code>
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
        url_fmt = "http://table.finance.yahoo.com/table.csv?a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&s=%s"
        y_t0, m_t0, d_t0, y_t1, m_t1, d_t1,code, self.outpath= self.parseInfo()
        url = url_fmt % (m_t0, d_t0, y_t0, m_t1, d_t1, y_t1, code)
        data = ""
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

    def importCode(self):
        fn = filedialog.askopenfilename(title='Open Stock Code List',filetype=[('Stock code list files','*.*')])
        try:
            with open(fn,'r',encoding='utf-8') as f:
                s = f.read()
                self.txtCodeList.insert(1.0,s)
        except:
            pass

    def parseHTML(self,html):
        re_market = re.compile(r'/(s[zh])(\d{6})\.html')
        re_name = re.compile(r'(.+)\(\d{6}\)')
        code_sz = ""
        code_sh = ""
        soup = BeautifulSoup(html,'html.parser')
        for li in soup.find('div',{'id':'quotesearch'}).find_all('li'):
            try:
                href = li.a['href']
                href_m = re_market.search(href)
                market,code = href_m.group(1),href_m.group(2)
                name = re_name.search(li.a.string).group(1)       
                if 'sz' == market:
                    code_sz += str(name)+'('+str(code)+')'+'\n'
                else:
                    code_sh += str(name)+'('+str(code)+')'+'\n'
            except:
                continue
        return code_sh,code_sz

    def getCodeList(self):
        # self.status.set('Please wait...')
        url = "http://quote.eastmoney.com/stocklist.html"
        codeList = ''
        try:
            r = requests.get(url,timeout=30)
            r.raise_for_status()
            r.encoding=r.apparent_encoding            
            codeList = self.parseHTML(r.text)
        except Exception as e:
            messagebox.showinfo(title='Error',message=e)
        content = '='*10+'Shanghai'+'='*10+'\n' + codeList[0]
        content += '='*10+'Shenzhen'+'='*10+'\n' + codeList[1]
        # self.txtCodeList.insert(1.0,'='*10+'Shanghai'+'='*10+'\n')
        # self.txtCodeList.insert('current',str(codeList[0]))
        # self.txtCodeList.insert('current','='*10+'Shenzhen'+'='*10+'\n')
        # self.txtCodeList.insert('current',str(codeList[1]))
        self.txtCodeList.insert(1.0,content)
        # self.status.set('')

    def exportCode(self):
        fn = filedialog.asksaveasfilename(title='Export Stock Code')
        try:
            with open(fn,'w',encoding='utf-8') as f:
                f.write(self.txtCodeList.get(1.0,'end'))
        except:
            pass

    def importData(self):
        path = filedialog.askopenfilename(title='Choose data',filetypes=[('csv files','.csv')])
        self.importPath.set(path)
        if len(path)>0:
            try:
                self.stock_df = pd.read_csv(path,sep=',',parse_dates=True,index_col='Date')                
                self.lbCols.set(tuple(self.stock_df.columns[:4]))
                self.lbSelectCol.selection_set(0)
                self.btnDraw.config(state=tk.NORMAL)
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
        figureTk.title(self.figtitle.get())
        # self.canvas.show()
        canvas = FigureCanvasTkAgg(self.fig, master=figureTk)
        canvas.get_tk_widget().grid(row=0,column=0)

        try:  
            self.stock_df.ix[:,cols].plot(ax=self.ax)        
            self.ax.set_title(self.figtitle.get())
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('Price')
        except:
            # messagebox.showinfo(title='Error',message=e)
            pass
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

