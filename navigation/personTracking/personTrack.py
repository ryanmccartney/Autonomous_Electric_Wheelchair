#NAME: personTrack.py
#DATE: 08/02/2019
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python function for navigating the wheelchair with an XBOX 360 game controller avoiding obstacles
#COPY: Copyright 2019, All Rights Reserved, Ryan McCartney

from personTracking import PersonTracking
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

try:
    #Open Configuration File
    configurationFile = open('testing/personTracking/settings.json').read()
    configuration = json.loads(configurationFile)

    #Get the details of the log file from the configuration
    logFilePath = configuration['general']['logFileDirectory']
    logFileName = configuration['general']['logFileName']
    logFileFullPath = logFilePath + logFileName

    #open a txt file to use for logging and clear it
    logFile = open(logFileFullPath,"w")
    logFile.close()

    log(logFileFullPath,"INFO = Program has started running.")
    log(logFileFullPath,"INFO = Main Thread has accessed log file.")

except:
    log(logFileFullPath,"ERROR = Log file could not be created.")
    log(logFileFullPath,"STATUS = Terminating Program.")
    exit()

#Initialise Image Processing Algorithm
try:
    personTrack = PersonTracking(configuration)

    try:
        personTrack.info = True
        personTrack.showFPS = True
        personTrack.showClock = True
        personTrack.displayStream = True

        personTrack.trackPeople()
        log(logFileFullPath,"INFO = Starting person tracking.")

        #Poll Tracking Status
        while 1:
            if(personTrack.status == False):
                exit()
            time.sleep(5)

    except:
        log(logFileFullPath,"ERROR = Could not initiate Person Tracking.")
        log(logFileFullPath,"STATUS = Terminating Program.")
        exit()

except:
    log(logFileFullPath,"ERROR = Could not initiate Person Detection Class.")
    log(logFileFullPath,"STATUS = Terminating Program.")
    exit()