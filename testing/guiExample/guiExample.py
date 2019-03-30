#NAME: guiExample.py
#DATE: 08/02/2019
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python function for navigating the wheelchair with an XBOX 360 game controller avoiding obstacles
#COPY: Copyright 2019, All Rights Reserved, Ryan McCartney

from control import Control
import tkinter as tk
import time
import json

#Logging Function (Pretty Console Output)
def log(logFilePath,entry):    

    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + entry

    #open a txt file to use for logging
    logFile = open(logFilePath,"a+")
    logFile.write(logEntry+"\n")
    logFile.close()
    print(logEntry)

def sendData(variable):
    wheelchair.transmitCommand(speed.get(),angle.get(),"RUN")

def refreshData():
    
    wheelchair.getUpdate()
    speed.set(wheelchair.setSpeed)
    angle.set(wheelchair.setAngle)

    batteryPercent["text"] = "Battery Voltage = "+str(wheelchair.batteryPercent())+"%"
    batteryVoltage["text"] = "Battery Voltage = "+str(wheelchair.batteryVoltage)+"V"
    powerUsage["text"] = "Current Power Usage = "+str(wheelchair.batteryVoltage)+"w"
    statusMessage["text"] = str(wheelchair.status)

    root.after(2000,refreshData) 

try:
    #Open Configuration File
    configurationFile = open('testing/guiExample/settings.json').read()
    configuration = json.loads(configurationFile)

    #Get the details of the log file from the configuration
    logFilePath = configuration['general']['logFile']

    #open a txt file to use for logging and clear it
    logFile = open(logFilePath,"w")
    logFile.close()

    log(logFilePath,"INFO = Main Thread has accessed log file.")

except:
    log(logFilePath,"ERROR = Log file could not be created.")
    exit()

#Initialise Control Class
try:
    wheelchair = Control(configuration)

    try:
        #Create GUI
        log(logFilePath,"INFO = Starting GUI.")

        root = tk.Tk()
        root.title("Teleprescence Control")

        #size of the window
        root.geometry("800x450")

        frame = tk.Frame(root)
        frame.pack()
        
        buttonStop = tk.Button(frame,text="Stop",fg="red", height=4, width=20, command=wheelchair.eStop)
        buttonStop.pack(side=tk.LEFT)

        buttonReset = tk.Button(frame,text="Reset",fg="green",height=4, width=20,command=wheelchair.reset)
        buttonReset.pack(side=tk.LEFT)

        speed = tk.Scale(root, from_=100, to=-100,tickinterval=5,length=200,command=sendData)
        speed.pack()
        
        angle = tk.Scale(root, from_=-100, to=100,tickinterval=5,orient=tk.HORIZONTAL,length=600,command=sendData)
        angle.pack()

        batteryVoltage = tk.Label(root, fg="black")
        batteryVoltage.pack()
        batteryVoltage.config(text="Battery Voltage = "+str(wheelchair.batteryVoltage)+"V")

        batteryPercent = tk.Label(root, fg="black")
        batteryPercent.pack()
        batteryPercent.config(text="Battery Voltage = "+str(wheelchair.batteryPercent())+"%")
        
        powerUsage = tk.Label(root, fg="black")
        powerUsage.pack()
        powerUsage.config(text="Current Power Usage = "+str(wheelchair.batteryVoltage)+"w")

        statusMessage = tk.Label(root, fg="black")
        statusMessage.pack()
        statusMessage.config(text=str(wheelchair.status))

        root.after(1, refreshData)
        root.mainloop()

    except:
        log(logFilePath,"ERROR = Could not initiate GUI.")
        log(logFilePath,"STATUS = Terminating Program.")
        exit()

except:
    log(logFilePath,"ERROR = Could not initiate Control class.")
    log(logFilePath,"STATUS = Terminating Program.")
    exit()