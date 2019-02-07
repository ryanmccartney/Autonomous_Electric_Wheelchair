#NAME: gamepadNavigationAntiCollision.py
#DATE: 07/02/2019
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python function for navigating the wheelchaitr with an XBOX 360 game controller avoiding obstacles
#COPY: Copyright 2019, All Rights Reserved, Ryan McCartney

from control import Control
from imageProcessing import imageProcessing
import json
import time

try:
    #Open Configuration File
    configurationFile = open("navigation\settings.json").read()
    configuration = json.loads(configurationFile)

    #Get the details of the log file from the configuration
    logFilePath = configuration['general']['logFileDirectory']
    logFileName = configuration['general']['logFileName']
    logFileFullPath = logFilePath + logFileName

    #open a txt file to use for logging 
    logFile = open(logFileFullPath,"w+")
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "INFO = Program has started running." + "\n"
    logFile.write(logEntry)
    print(logEntry)

except:
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "ERROR = Log file could not be created." + "\n"
    print(logEntry)

#Initialise Image Processing Algorithm
try:
    antiCollision = imageProcessing(configuration)

    try:
        antiCollision.processStream()

        #Intialise Control Session for Wheelchair
        try:
            wheelchair = Control(configuration)

            while antiCollision.processing == True:

            
            #write status to log file
            currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
            logEntry = currentDateTime + ": " + "INFO = Control Connection Established with Robotic Device." + "\n"
            logFile.write(logEntry)
            print(logEntry)
    
        except:
            #write status to log file
            currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
            logEntry = currentDateTime + ": " + "ERROR = Could not create a control instance for the wheelchair." + "\n"
            logFile.write(logEntry)
            print(logEntry)

except:
    #write status to log file
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "ERROR = Could not Initialise the Image Processing Class." + "\n"
    logFile.write(logEntry)
    print(logEntry)



  
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

