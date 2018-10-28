#NAME:  move.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for moving the wheelchair in an intuative manner
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

import numpy as np
import time
import urllib
import csv

class move:

    batteryVoltage = 0
    rightMotorCurrent = 0
    leftMotorCurrent = 0
    status = 0 
    logFile = "log.csv"

    previousSpeed = 0 

    def __init__(self,host):

        #Open Connection
        urllib.urlopen(self.host)
       
        # opening the file, clearing and applying headings
        with open(logFile, 'rb') as file:

          file.write("Battery Voltage(V),Right Current (A),Left Current (A),Status Message")

    def transmitData(self, speed, angle, command):

        command_url = self.host + speed + ',' + angle + ',' + command + '/r/n'
        data = urllib.urlopen(self.host)
        
        if data != NULL:

            parse data

    #Method to allow data to logged to a file 
    def logData(self):   

        #Create string to write to file
        dataEntry = batteryVoltage + ',' + rightMotorCurrent + ',' + leftMotorCurrent + ',' + status

        #Open file and wirte string
        with open(logFile, 'a') as file:
          file.write(dataEntry)
        

    def rampSpeed(self,speed):
        
       #Accelerate
        if speed > self.previousSpeed:

            while speed != self.previousSpeed:
            
                speed = self.previousSpeed + 1
                transmitData (speed,self.angle,"SEND")

        #Decelerate
        else if speed < self.previousSpeed:

            while speed != self.previousSpeed:
            
                speed = self.previousSpeed - 1
                transmitData (speed,self.angle,"SEND")
            
        return speed
    