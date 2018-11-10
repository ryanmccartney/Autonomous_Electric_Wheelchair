#NAME:  main.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for aquiring image data from network streams
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

from cameraData import cameraData
from navigation import Navigation
from threading import Thread
from queue import Queue
import cv2 as cv
import json
import time

#--------------------------------------------------------------------------------
# Load user adjustable variables from json file
#--------------------------------------------------------------------------------

#open a txt file to use for logging 
logFile = open("log.txt","w+")
currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
logEntry = currentDateTime + ": " + "INFO = Program has started running." + "\n"
logFile.write(logEntry)

#load settings file
settingsFile = open('navigation\settings.json').read()
settings = json.loads(settingsFile)

#write status to log file
currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
logEntry = currentDateTime + ": " + "INFO = Settings file loaded." + "\n"
logFile.write(logEntry)

#Resolution of matrix
unitSize = settings['map']['unitSize']

#Map Length, Width and Height (in milimeters)
mapLength = settings['map']['length']
mapWidth = settings['map']['width']
mapHieght = settings['map']['hieght']

#write status to log file
currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
logEntry = currentDateTime + ": " + "INFO = Map created." + "\n"
logFile.write(logEntry)

#--------------------------------------------------------------------------------
#Data Streams Setup
#--------------------------------------------------------------------------------

#Assign URLs from Settings File to Variables
kinectImage_url = settings['host']['kinectImage_url']
kinectDepth_url = settings['host']['kinectDepth_url']
webcam_url = settings['host']['webcam_url']
test_url = settings['host']['test_url']


#write status to log file
currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
logEntry = currentDateTime + ": " + "INFO = Loading camera streams." + "\n"
logFile.write(logEntry)

#Class instances for various streams
#kinectImage = cameraData(kinectImage_url,"Kinect RGB Data")
kinectDepth = cameraData(test_url,"Kinect Depth Data")

#Stream Data
#kinectImage.streamVideo()
#kinectDepth.streamVideo()

#write status to log file
currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
logEntry = currentDateTime + ": " + "STATUS = Camera streams loaded." + "\n"
logFile.write(logEntry)

#--------------------------------------------------------------------------------
#Intialise Navigation Techniques
#--------------------------------------------------------------------------------

#Initilise Class
navigate = Navigation(unitSize,mapLength,mapWidth,mapHieght)

#Start Closest Point in Path Analysis
navigate.closestPoint(test_url,True)

while 1:

    #write status to log file
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "INFO = Processing Depth Data" + "\n"
    logFile.write(logEntry)
    
    depthFrame = kinectDepth.getFrame()
    cv.imshow('Original Depth Frame',depthFrame)

    #mappedDepth = map.mapFrameSlow(depthFrame)
    #map.plotPointCloud(mappedDepth)
    #map.writeCSV(mappedDepth)
    
    # quit program when 'esc' key is pressed
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()

    