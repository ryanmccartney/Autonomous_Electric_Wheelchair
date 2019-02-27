#NAME: autoCircle.py
#DATE: 12/11/2018
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python class for moving the wheelchair in a circle whilst avoiding collisoins
#COPY: Copyright 2018, All Rights Reserved, Ryan McCartney

from control import Control
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
    
    #Carry out control command
    try:
        
        #Full Circle
        wheelchair.changeAngle(80)
        #Speed up
        wheelchair.rampSpeed(50,100)
        #Change Radius
        #wheelchair.changeRadius(30)
        #wheelchair.changeRadius(50)
        
        #Wait 60 Seconds
        time.sleep(60)

        #Reduce Speed
        wheelchair.rampSpeed(0,100)
        
        wheelchair.eStop()
        exit()

    except:
         #write status to log file
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "ERROR = Unable to adjust wheelchair speed." + "\n"
        logFile.write(logEntry)
        print(logEntry)

except:
    #write status to log file
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "ERROR = Could not create a control instance for the wheelchair." + "\n"
    logFile.write(logEntry)
    print(logEntry)
    exit()

   
   