#NAME: autoCircle.py
#DATE: 12/11/2018
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python class for moving the wheelchair in a circle whilst avoiding collisoins
#COPY: Copyright 2018, All Rights Reserved, Ryan McCartney

from control import Control
import json
import time

#Create a file for logging
try:
    #open a txt file to duse for logging 
    logFile = open("navigation\circleNavigate\circleLog.txt","w+")
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
    settings = json.loads(settingsFile)
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

#Extract Data from settings file
try: 
    control_url = settings['host']['command_url']
    kinectImage_url = settings['host']['kinectImage_url']
    kinectDepth_url = settings['host']['kinectDepth_url']
    webcam_url = settings['host']['webcam_url']
    test_url = settings['host']['test_url']
    
    #write status to log file
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "INFO = Data extracted successfully from settings file." + "\n"
    logFile.write(logEntry)
    print(logEntry)
except:
    #write status to log file
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "ERROR = Unable to extract data from settings file. Is data in the correct format?" + "\n"
    logFile.write(logEntry)
    print(logEntry)
    exit()

#Intialise Control Session for Wheelchair
try:
    #Initialise Class for control
    wheelchair = Control(control_url)
    #write status to log file
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "INFO = Control Connection Established with Robotic Device." + "\n"
    logFile.write(logEntry)
    print(logEntry)

    #Carry out control command
    try:

        #Full Circle
        wheelchair.changeAngle(100)
        #Increase Speed
        wheelchair.rampSpeed(30,1)
        #Reduce Speed
        wheelchair.rampSpeed(0,1)
        #Anticlockwise
        wheelchair.changeAngle(-100)
        #Increase Speed
        wheelchair.rampSpeed(30,1)
        #Emergency Stop Wheelchair
        wheelchair.eStop()

        exit()

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

