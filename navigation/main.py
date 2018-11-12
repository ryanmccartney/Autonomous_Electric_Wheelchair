#NAME: main.py
#DATE: 12/11/2018
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: Main python script for automous navigation of a two wheeled robot.
#COPY: Copyright 2018, All Rights Reserved, Ryan McCartney

from cameraData import cameraData
from navigation import Navigation
from control import Control
from threading import Thread
from queue import Queue
import cv2 as cv
import json
import time

#Create a file for logging
try:
    #open a txt file to use for logging 
    logFile = open("log.txt","w+")
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
    #Data from settings file
    unitSize = settings['map']['unitSize']
    mapLength = settings['map']['length']
    mapWidth = settings['map']['width']
    mapHieght = settings['map']['hieght']
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


#Get camera data
try: 
    #Class instances for various streams
    #kinectImage = cameraData(kinectImage_url,"Kinect RGB Data")
    kinectDepth = cameraData(test_url,"Kinect Depth Data")

    #Stream Data
    #kinectImage.streamVideo()
    #kinectDepth.streamVideo()

    #write status to log file
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "INFO = Camera data acquired succesfully." + "\n"
    logFile.write(logEntry)
    print(logEntry)
except:
    #write status to log file
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "ERROR = Unable to acquire camera data. Check stream URLs in settings file." + "\n"
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
        #Ramp Speed
        wheelchair.rampSpeed(100,100)
    except:
         #write status to log file
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "ERROR = Unable to adjust wheelchair speed." + "\n"
        logFile.write(logEntry)
        print(logEntry)

except:
    #write status to log file
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "ERROR = Unable to establish connection with Robotic Deivce." + "\n"
    logFile.write(logEntry)
    print(logEntry)

#Intialise Navigation Techniques
try:
    #Intialise Class
    navigate = Navigation(unitSize,mapLength,mapWidth,mapHieght)

    #Adjust Scall Factor to Improve Optimisation
    navigate.scaleFactor = 2
    navigate.fps = 60
    delay = 1/navigate.fps
    #Start Closest Point in Path Analysis
    navigate.closestPoint(test_url,True)
    
    #write status to log file
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "INFO = Navigation started sucessfully." + "\n"
    logFile.write(logEntry)
    print(logEntry)

except:
    #write status to log file
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "ERROR = Unable to begin navigation." + "\n"
    logFile.write(logEntry)
    print(logEntry)

previousMaxSpeed = 0
pointCloud = 0
frames = 25

while 1:

    #Write Max Speed to Log File
    if navigate.maxSpeed != previousMaxSpeed:
        #write status to log file
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "STATUS = The Maximum Wheelchair Speed has been set as "+str(navigate.maxSpeed)+ "\n"
        logFile.write(logEntry)
        previousMaxSpeed = navigate.maxSpeed
    
    depthFrame = kinectDepth.getFrame()
    cv.imshow('Original Depth Frame',depthFrame)

    if frames ==25:
        pointCloud = navigate.createPointCloud(depthFrame)
        #navigate.plotPointCloud(pointCloud)
        #navigate.writeCSV(pointCloud)

        frames = 0

    #Delay for video frame
    time.sleep(delay)
    frames = frames + 1

    # quit program when 'esc' key is pressed
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()