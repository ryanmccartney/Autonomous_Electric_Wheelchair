#NAME: gamepadNavigation.py
#DATE: 12/11/2018
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python function for navigating the wheelchaitr with an XBBOX 360 game controller
#COPY: Copyright 2019, All Rights Reserved, Ryan McCartney

from control import Control
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

try:
    #Open Configuration File
    configurationFile = open('navigation/settings.json').read()
    configuration = json.loads(configurationFile)

    #Get the details of the log file from the configuration
    logFilePath = configuration['general']['logFileDirectory']
    logFileName = "gamepadNavigation.txt"
    logFileFullPath = logFilePath + logFileName

    #open a txt file to use for logging and clear it
    logFile = open(logFileFullPath,"w")
    logFile.close()

    #open a txt file to use for logging
    log(logFileFullPath,"INFO = Gamepad navigation program has started running.")

except:
    log(logFileFullPath,"ERROR = Log file could not be created.")

#Intialise Control Session for Wheelchair
try:
    #Initialise Class for control
    wheelchair = Control(configuration)
    
    #write status to log file
    log(logFileFullPath,"INFO = Control Connection Established with Robotic Device.")

    #Carry out control command
    try:

        while wheelchair.connected == True:

            if wheelchair.gamepadRunning == False:
                wheelchair.gamepadRunning = True
            
            wheelchair.gamepadRunning = True
            wheelchair.getUpdate()
            time.sleep(1)

        wheelchair.eStop()
        exit()

    except:
        #write status to log file
        log(logFileFullPath,"ERROR = Unable to send commands to the wheelchair.")
        wheelchair.eStop()
        exit()

except:
    #write failed initialise control class log
    log(logFileFullPath,"ERROR = Unable connect to the wheelchair for control. Is it turned on or are you connected to the same network?")
    exit()

