#NAME:  main.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for aquiring image data from network streams
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

from cameraData import cameraData
from mapDepth import mapDepth
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
logFile.write(currentDateTime,": INFO = Program has started running.\r\n")

#load settings file
settingsFile = open('navigation\settings.json').read()
settings = json.loads(settingsFile)

#write status to log file
currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
logFile.write(currentDateTime,": INFO = Settings file loaded.\r\n")

#Resolution of matrix
unitSize = settings['map']['unitSize']

#Map Length, Width and Height (in milimeters)
mapLength = settings['map']['length']
mapWidth = settings['map']['width']
mapHieght = settings['map']['hieght']

#write status to log file
currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
logFile.write(currentDateTime,": INFO = Map created.\r\n")

#--------------------------------------------------------------------------------
#Data Streams Setup
#--------------------------------------------------------------------------------


#write status to log file
currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
logFile.write(currentDateTime,": INFO = Loading camera streams.\r\n")

kinectImage_url = settings['host']['kinectImage_url']
kinectDepth_url = settings['host']['kinectDepth_url']
webcam_url = settings['host']['webcam_url']

#write status to log file
currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
logFile.write(currentDateTime,": STATUS = Camera streams loaded.\r\n")

#Class instances for various streams
#kinectImage = cameraData(kinectImage_url,"Kinect RGB Data")
kinectDepth = cameraData(kinectDepth_url,"Kinect Depth Data")
#webcam = cameraData(webcam_url,"Webcam")

#Stream Data
#kinectImage.streamVideo()
#kinectDepth.streamVideo()

#--------------------------------------------------------------------------------
#Map Depth Data to 3D Matrix
#--------------------------------------------------------------------------------

map = mapDepth(unitSize,mapLength,mapWidth,mapHieght)

#Set the Frame Size
map.readFrameSize(kinectDepth.getFrame())

while 1:
    
    depthFrame = kinectDepth.getFrame()
    mappedDepth = map.mapFrame(depthFrame)
    
    cv.imshow('Original Depth Frame',depthFrame)

    map.plotPointCloud(mappedDepth)
    #map.writeCSV(mappedDepth)

    time.sleep(2)
    
    # quit program when 'esc' key is pressed
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()

    