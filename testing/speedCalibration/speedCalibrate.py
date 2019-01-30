#NAME: captureClick.py
#DATE: 15/01/2019
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: Python Script CConverting Kinect Data to Real World Coordinated
#COPY: Copyright 2018, All Rights Reserved, Ryan McCartney


import cv2 as cv
import numpy as np
import numba as nb
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from control import Control
import time
import math
import threading

#define threading wrapper
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper
    
#returnValue
def pixelValue(event, x, y, flags, param):

    if event == cv.EVENT_LBUTTONDOWN:
        elementValue = depthValues[y,x]
        distance = distanceCalc(elementValue)
        print("INFO The value of the selected pixel is",elementValue,"and the distance is estimated distance is %.2fm."%round(distance,2))

#Processing Loop
@threaded
def processVideo(depthPath,videoPath):

    global depthValues
    global closestObject
    global depthProcessing
    
    depthProcessing = False

    #Depth and Video Data
    depth = cv.VideoCapture(depthPath)
    video = cv.VideoCapture(videoPath)
    
    depthProcessing = True
    while(depth.isOpened()):

        ret, depthFrame = depth.read()
 
        #Process Depth Image
        depthFrame = cv.cvtColor(depthFrame, cv.COLOR_BGR2GRAY)

        #Assign Values
        closestPoint = scanImage(depthFrame)
        closestObject = closestPoint[0]

        cv.imshow('Streamed Depth Data',depthFrame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    depthProcessing = False
    depth.release()
    video.release()
    cv.destroyAllWindows()

#Optimised method for finding the closest point in an image
@nb.jit(nopython=True)
def scanImage(depthData):

    height = len(depthData)
    width = len(depthData[0])

    #Initialise with worst case
    pointValue = 1023
    pointHeight = 0
    pointWidth = 0

    #Threshold for dealing with annomolies (reflective surfaces)
    threshold = 0

    #Populate Array with Data
    for h in range (0,height):

        for w in range (0,width):

            if  (depthData[h,w] <= pointValue) and (depthData[h,w] >= threshold):
                pointValue = depthData[h,w]
                pointHeight = h
                pointWidth = w
                
    results = [pointValue, pointWidth, pointHeight]
    return results

#Returns infomraiton about how far away a point is in and image
def distanceCalc(depth):

    cameraAngle = 60
    vehicleLength = 0.45

    a = -0.0000000069
    b = 0.0000064344
    c = -0.0019066199
    d = 0.2331614352
    e = -9.5744837865
    #Second Order Custom Estimation
    distance = (a*math.pow(depth,4))+(b*math.pow(depth,3))+(c*math.pow(depth,2))+(d*depth)+e

    #First Order Custom Estimation
    #m = 0.0161
    #c = -1.4698
    #distance = (m*depth)+c

    #Simple trig to create ground truth distance 
    cameraAngle = math.radians(cameraAngle)
    groundDistance = math.sin(cameraAngle)*distance
    groundDistance = groundDistance - vehicleLength
    
    return groundDistance

#------------------------------------------------------------------------------------------
#Main Script
#------------------------------------------------------------------------------------------

depthPath = "navigation\kinect\KinectDepth_testData2.avi"
videoPath = "navigation\kinect\KinectRGB_testData2.avi"
closestObject = 3
depthProcessing = False

depthStream = "http://192.168.1.100:8081/?action=stream"
videoStream = "http://192.168.1.100:8080/?action=stream"
controlURL = "http://192.168.1.100/scripts/serialSend.php?serialData="


#Initialise Class for control
wheelchair = Control(controlURL)

#Start Image Processing
processVideo(depthStream,videoStream)

while 1:

    if depthProcessing == True:

        print("INFO: Depth Processing has Begun.")

        #TRIAL
        #Full Circle
        wheelchair.changeAngle(100)
        #Increase Speed
        wheelchair.rampSpeed(30,2)
        #Reduce Speed
        wheelchair.rampSpeed(0,2)
        #Anticlockwise
        wheelchair.changeAngle(-100)
        #Increase Speed
        wheelchair.rampSpeed(30,2)
        #Emergency Stop Wheelchair
        wheelchair.eStop()

        exit()

        wheelchair.transmitCommand(8,0,"SEND")
        start = time.time()

        while depthProcessing == True:
            if closestObject < 0.4:
                print("INFO: A distance of",closestObject,"meters has been reached.")
                wheelchair.transmitCommand(0,angle,"STOP")
                end = time.time()
                print("STATUS: It took %.2f seconds for the wheelchair to react to the object" % round((end-start),3))
                exit()

        wheelchair.transmitCommand(0,0,"STOP")



