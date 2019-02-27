#NAME: gamepadNavigation.py
#DATE: 12/11/2018
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python function for navigating the wheelchaitr with an XBBOX 360 game controller
#COPY: Copyright 2019, All Rights Reserved, Ryan McCartney

from control import Control
import json
import time

#Create a file for logging
try:
    #open a txt file to use for logging 
    logFile = open("data\logs\gamepadNavigation.txt","w+")
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "INFO = Program has started running." + "\n"
    logFile.write(logEntry)
    print(logEntry)
except:
    print("ERROR: Unable to open log file.")
    exit()

#Import Settings File
try: 
    #load settings file
    settingsFile = open('navigation\settings.json').read()
    configuration = json.loads(settingsFile)
    #write status to log file
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "INFO = Settings file loaded." + "\n"
    logFile.write(logEntry)
    print(logEntry)
except:
    #write status to log file
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "ERROR = Unable to open the settings file." + "\n"
    logFile.write(logEntry)
    print(logEntry)
    exit()

#Intialise Control Session for Wheelchair
try:
    #Initialise Class for control
    wheelchair = Control(configuration)
    #write status to log file
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "INFO = Control Connection Established with Robotic Device." + "\n"
    logFile.write(logEntry)
    print(logEntry)

    #Carry out control command
    try:
        
        while 1:
            wheelchair.gamepadRunning = True

    except:
         #write status to log file
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "ERROR = Unable to adjust wheelchair speed." + "\n"
        logFile.write(logEntry)
        print(logEntry)

except:
    #write failed initialise control class log
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "ERROR = Unable connect to the wheelchair for control. Is it turned on or are you connected to the same network?" + "\n"
    logFile.write(logEntry)
    print(logEntry)
    exit()

