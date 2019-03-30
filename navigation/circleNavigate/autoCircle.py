#NAME: autoCircle.py
#DATE: 12/11/2018
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python class for moving the wheelchair in a circle whilst avoiding collisoins
#COPY: Copyright 2018, All Rights Reserved, Ryan McCartney

from control import Control
import tkinter as tk
import json
import time

#Logging Function (Pretty Console Output)
def log(logFilePath,entry):    

    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + entry

    #open a txt file to use for logging
    logFile = open(logFilePath,"a+")
    logFile.write(logEntry+"\n")
    logFile.close()
    print(logEntry)

#Create GUI
root = tk.Tk()
root.title("Circle Control")

try:
    #Open Configuration File
    configurationFile = open('navigation/settings.json').read()
    configuration = json.loads(configurationFile)

    #Get the details of the log file from the configuration
    logFilePath = configuration['general']['logFileDirectory']
    logFileName = "circle.txt"
    logFileFullPath = logFilePath + logFileName

    #open a txt file to use for logging and clear it
    logFile = open(logFileFullPath,"w")
    logFile.close()

    #open a txt file to use for logging
    log(logFileFullPath,"INFO = Program has started running.")

except:
    log(logFileFullPath,"ERROR = Log file could not be created.")

#Intialise Control Session for Wheelchair
try:
    wheelchair = Control(configuration)

    #write status to log file
    log(logFileFullPath,"INFO = Control Connection Established with Robotic Device.")

    #Debugging
    wheelchair.debug = False
    
    #Carry out control command
    try:

        frame = tk.Frame(root)
        frame.pack()

        buttonStop = tk.Button(frame,text="Stop",fg="red",command=wheelchair.eStop)
        buttonStop.pack(side=tk.LEFT)

        buttonReset = tk.Button(frame,text="Reset",fg="green",command=wheelchair.reset)
        buttonReset.pack(side=tk.LEFT)

        

        #Full Circle
        wheelchair.changeAngle(100)
        
        while wheelchair.connected == True:

            #Speed up
            wheelchair.rampSpeed(40,200)
            #Wait 60 Seconds
            time.sleep(2)
            #Slow Down
            wheelchair.rampSpeed(10,200)
            #Wait 60 Seconds
            time.sleep(2)
            
            #Change Radius
            #wheelchair.changeRadius(30)
            #wheelchair.changeRadius(50)
        
        wheelchair.eStop()
        exit()

    except:
         #write status to log file
         log(logFileFullPath,"ERROR = Unable to adjust wheelchair speed")
         wheelchair.eStop()

except:
    #write status to log file
    log(logFileFullPath,"ERROR = Could not create a control instance for the wheelchair.")
    exit()

root.mainloop()
   