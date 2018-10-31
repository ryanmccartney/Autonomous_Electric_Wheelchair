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

settingsFile = open('navigation\settings.json').read()
settings = json.loads(settingsFile)

#Resolution of matrix
unitSize = settings['map']['unitSize']

#Map Length, Width and Height (in milimeters)
mapLength = settings['map']['length']
mapWidth = settings['map']['width']
mapHieght = settings['map']['hieght']

#--------------------------------------------------------------------------------
#Data Streams Setup
#--------------------------------------------------------------------------------

kinectImage_url = settings['host']['kinectImage_url']
kinectDepth_url = settings['host']['kinectDepth_url']
webcam_url = settings['host']['webcam_url']

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

    map.plotMap(mappedDepth)

    time.sleep(2)
    
    # quit program when 'esc' key is pressed
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()

    