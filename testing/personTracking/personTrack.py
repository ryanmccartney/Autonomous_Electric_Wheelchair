#NAME: personTrack.py
#DATE: 08/02/2019
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python function for navigating the wheelchair with an XBOX 360 game controller avoiding obstacles
#COPY: Copyright 2019, All Rights Reserved, Ryan McCartney

from personTracking import PersonTracking
import time
import json

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
    personTrack = PersonTracking(configuration)

    try:
        personTrack.info = True
        personTrack.fps = True

        while 1:
            personTrack.trackPeople()

    except:
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "ERROR = Could not initiate Person Tracking." + "\n"
        print(logEntry)
        exit()

except:
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "ERROR = Could not initiate Person Detection Class." + "\n"
    print(logEntry)
    exit()
