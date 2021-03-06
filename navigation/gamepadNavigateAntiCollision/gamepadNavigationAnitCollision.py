
#NAME: gamepadNavigationAntiCollision.py
#DATE: 08/02/2019
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python function for navigating the wheelchaitr with an XBOX 360 game controller avoiding obstacles
#COPY: Copyright 2019, All Rights Reserved, Ryan McCartney

from control import Control
from imageProcessing import imageProcessing
import json
import time

try:
    #Open Configuration File
    configurationFile = open('navigation/settings.json').read()
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

            #write status to log file
            currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
            logEntry = currentDateTime + ": " + "INFO = Control Connection Established with Robotic Device." + "\n"
            logFile.write(logEntry)
            print(logEntry)

            #Uncomment to Debug
            #antiCollision.debug = True
            #wheelchair.debug = True
            while 1:
                while antiCollision.processing == True:

                    wheelchair.gamepadRunning = True

                    wheelchair.calcMaxSpeed(antiCollision.closestObject)

        except:
            #write status to log file
            currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
            logEntry = currentDateTime + ": " + "ERROR = Could not create a control instance for the wheelchair." + "\n"
            logFile.write(logEntry)
            print(logEntry)
            exit()

    except:
        #write status to log file
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "ERROR = Could not start processing any imagery." + "\n"
        logFile.write(logEntry)
        print(logEntry)
        exit()

except:
    #write status to log file
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "ERROR = Could not initialise the image processing class." + "\n"
    logFile.write(logEntry)
    print(logEntry)
    exit()