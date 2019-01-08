# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 19:34:47 2017

@author: cada
"""

import serial
import tkinter as tk
from tkinter import ttk
import time
import sys


import matplotlib
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style



class Measure(object):
    def __init__(self):
         self.data = list()
         self.data.append("vlhkost:teplota:pocit_teplota")
         self.serStatus()
    
    def serStatus(self):
        try:
            ser = serial.Serial('COM7', 9600)
            if ser.is_open:
                print("port is open, closing")
                for i in range(10):
                    time.sleep(0.1)
                    ser.write('0'.encode())
                ser.close()
        except Exception as e:
            print(e)

    def measure_on(self):
       ser = serial.Serial('COM7', 9600)
       print("port open = ", ser.is_open)
       ser.flushInput() #flush input buffer, discarding all its contents
       ser.flushOutput()#flush output buffer, aborting current output 
                     #and discard all that is in buffer
       for i in range(10):
        ser.write('1'.encode())
        time.sleep(0.2)
        bytesToRead = ser.inWaiting()
        if (bytesToRead > 5):
           serial_line = ser.readline(bytesToRead)
           raw = serial_line.decode().strip()
           if len(raw) > 15:
               self.data.append(raw)
               self.backupFile(raw)
           else:
               pass
#               self.data.append("none")
           print(self.data[-1])

       ser.close()
       
       print("port open = ", ser.is_open)
       
    def backupFile(self, newLine):
        try:
            f = open("data.txt", "a")
            f.write(newLine + "\n")
            f.close()
        except Exception as e:
            print(e)
           
def animate(i):
    pullData = open('data.txt','r').read()

    dataArray = pullData.split('\n')
#    dataArray = m.data
    data1=[]
    data2=[]
    data3=[]
    vlhkost = []
    teplota = []
    pocitT = []
#    print("len data", len(dataArray))
    try:
        for line in dataArray:
            if len(line)>1:
                data1,data2, data3 = line.split(':')
                vlhkost.append(float(data1))
                teplota.append(float(data2))
                pocitT.append(float(data3))
        
        a.clear()
        a.plot(teplota)
        a.plot(vlhkost)
        a.plot(pocitT)
    except Exception as e:
        print("data file is empty")
        print("traceback", e)
    
        
    
def get(self,out):
    global data_out
    data_out.append(out)
    print(get)
    
    
class MeasureGui(tk.Tk):
    
    def __init__(self,*args, **kwargs):
         tk.Tk.__init__(self, *args, **kwargs)
         tk.Tk.title(self, "monitor")
         tk.Tk.minsize(self, width = 600, height = 600)
         tk.Tk.maxsize(self, width = 800, height = 800)
#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand = True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)
         
         buttonframe = tk.Frame(self)
         graphframe = tk.Frame(self)
         Button = tk.Button
         m = Measure()
         
         btn = Button(buttonframe, text = "measure ON ", width = 15, height = 2, command = m.measure_on)
        # btn1 = Button(buttonframe, text = "measure OFF ", width = 15, height = 2, command = measure_off)
         btn3 = Button(buttonframe, text = "quit", width = 15, height = 2, command = self.quit_app)
          
         btn.pack(side=tk.TOP, anchor=tk.N)
        # btn1.pack(side=tk.TOP, anchor=tk.N)
         btn3.pack(side=tk.TOP, anchor=tk.N)
         buttonframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
         canvas = FigureCanvasTkAgg(f, self)
         canvas.show()
         canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
         graphframe.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)
        # canvas.get_tk_widget().grid(row = 3, column = 0, sticky = "w")
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
    def quit_app(self):
        self.destroy()
        
        
def main():
 LARGE_FONT= ("Verdana", 12)
 style.use("ggplot")
 global a, f
 f = Figure(figsize=(8,4), dpi=100)
 a = f.add_subplot(111)
 
 app = MeasureGui()

 
 ani = animation.FuncAnimation(f, animate, interval=10)

 app.mainloop()
 
if __name__ == "__main__":
    main()




