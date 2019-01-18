# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 20:56:19 2018

@author: cada
"""

import serial
from vpython import * #Import all the vPython library

serialData = serial.Serial('COM7',9600) 

measuringRod = cylinder( title="My Meter", radius= .5, length=6, color=color.yellow)
target=box(pos=(0,-.5,0), length=.2, width=3, height=3, color=color.green)
while (1==1):
    rate(20)
    if (serialData.inWaiting()>0):
        myData = serialData.readline().decode().strip().split() #Read the distance measure as a string
        print(myData) #Print the measurement to confirm things are working
        if len(myData) > 1:
            distance = float(myData[1]) #convert reading to a floating point number
            measuringRod.length=distance #Change the length of your measuring rod to your last measurement
