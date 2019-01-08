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

LARGE_FONT= ("Verdana", 12)
style.use("ggplot")
f = Figure(figsize=(8,4), dpi=100)
a = f.add_subplot(111)
#update = 0

def quit_app():
    root.destroy()


def get(out):
    global data_out
    data_out.append(out)
    print(get)
    
def serStatus():
    try:
        ser = serial.Serial('COM7', 9600)
        if ser.is_open:
            print("serial is open, closing")
            ser.close()
    except:
        pass
#def measure_off():
#   loop=0
#   ser = serial.Serial('COM7', 9600)
#   print("port open = ", ser.is_open)
#   for i in range(10):
#    time.sleep(0.1)
#    ser.write('0'.encode())
#   ser.close()
#   print("port open = ", ser.is_open)

def measure_on():
   global data2
   data2 = list()
   serStatus()
   data2.append("vlhkost:teplota:pocit_teplota")
   i = 0
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
       data2.append(raw)
       print(data2[-1])
#       loop += 1
    #data2.append(0)
   ser.close()
#   update = 1
   print("port open = ", ser.is_open)
   
def animate(i):
    pullData = open('data.txt','r').read()
    dataArray = pullData.split('\n')
    xar=[]
    yar=[]
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    a.clear()
    a.plot(xar,yar)
    
def data_up():
    if (update == 0):
        print("no changes")
        
        
        
        
    
def main():
 global root
 root = tk.Tk()
 root.title("home_monitor")
 root.minsize(width = 600, height = 600)
 root.maxsize(width = 800, height = 800)
 buttonframe = tk.Frame(root)
 graphframe = tk.Frame(root)
 
 Button = tk.Button

 btn = Button(buttonframe, text = "measure ON ", width = 15, height = 2, command = measure_on)
# btn1 = Button(buttonframe, text = "measure OFF ", width = 15, height = 2, command = measure_off)
 btn3 = Button(buttonframe, text = "quit", width = 15, height = 2, command = quit_app)
  
# buttonframe.grid(row=3, column=0, columnspan=2)     
# btn.grid(row = 1, column = 1)
# btn1.grid(row = 1, column = 2)
# btn3.grid(row= 1, column = 3)
 btn.pack(side=tk.TOP, anchor=tk.N)
# btn1.pack(side=tk.TOP, anchor=tk.N)
 btn3.pack(side=tk.TOP, anchor=tk.N)
 buttonframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
# btn.place(relx=.1, rely=.04)
# btn1.pack(padx=30, pady=50, side=tk.LEFT)
# btn3.pack(padx=5, pady=0, side=tk.LEFT)
#
 canvas = FigureCanvasTkAgg(f, root)
 canvas.show()
 canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
 graphframe.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)
# canvas.get_tk_widget().grid(row = 3, column = 0, sticky = "w")

# ani = animation.FuncAnimation(f, animate, interval=1000)

 data_up()
 root.mainloop()
 print(data2)
if __name__ == "__main__":
    main()




