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
import time
import math

#returnValue
def pixelValue(event, x, y, flags, param):

    if event == cv.EVENT_LBUTTONDOWN:
        elementValue = depthValues[y,x]
        distance = distanceCalc(elementValue)
        print("The value of the selected pixel is",elementValue,"and the distance is estimated distance is %.2fm."%round(distance,2))

#Processing Loop
def processVideo(depthPath,videoPath,fps):

    global depthValues

    delay = 1/fps
    fpsActual = fps

    #Depth and Video Data
    depth = cv.VideoCapture(depthPath)
    video = cv.VideoCapture(videoPath)
 
    #Crosshair Size
    crosshairHeight = 10
    crosshairWidth = 10

    #For Mouse Click
    cv.namedWindow('Depth Data from File')
    cv.setMouseCallback('Depth Data from File',pixelValue)

    while(depth.isOpened()) and (video.isOpened()):

        start = time.time()

        ret, depthFrame = depth.read()
        ret, videoFrame = video.read()

        #Process Depth Image
        depthFrame = cv.cvtColor(depthFrame, cv.COLOR_BGR2GRAY)
        depthValues = depthFrame

        closestPoint = scanImage(depthFrame)
        distance = distanceCalc(closestPoint[0])

        #Convert Back to Colour
        depthFrame = cv.cvtColor(depthFrame,cv.COLOR_GRAY2RGB)

        #Add text with measurements
        font = cv.FONT_HERSHEY_SIMPLEX
        text = 'Closest point is %.2fm away.'%round(distance,2)
        cv.putText(videoFrame,text,(16,20), font, 0.6,(255,0,0),1,cv.LINE_AA)
        text = '%.2ffps'%round(fpsActual,2)
        cv.putText(videoFrame,text,(16,44), font, 0.6,(255,0,0),1,cv.LINE_AA)

        #Horizontal Line & Vertical Line on Video Image
        cv.line(videoFrame,((closestPoint[1]-crosshairWidth),closestPoint[2]),((closestPoint[1]+crosshairWidth),closestPoint[2]),(0,255,0),2)
        cv.line(videoFrame,(closestPoint[1],(closestPoint[2]-crosshairHeight)),(closestPoint[1],(closestPoint[2]+crosshairHeight)),(0,255,0),2)

        #Apply Colour Map
        depthFrame = cv.applyColorMap(depthFrame, cv.COLORMAP_JET)

        #Horizontal Line & Vertical Line on Depth Image
        cv.line(depthFrame,((closestPoint[1]-crosshairWidth),closestPoint[2]),((closestPoint[1]+crosshairWidth),closestPoint[2]),(0,255,0),2)
        cv.line(depthFrame,(closestPoint[1],(closestPoint[2]-crosshairHeight)),(closestPoint[1],(closestPoint[2]+crosshairHeight)),(0,255,0),2)

        #Show the images
        cv.imshow('Depth Data from File',depthFrame)
        cv.imshow('Image Data from File',videoFrame)

        end = time.time()
        #print("INFO: Processing duration for frame is %.2f seconds and the closest point is %.2f meters away." % (round((end-start),2), round(distance,2)))
        adjustedDelay = delay-(end-start)

        if adjustedDelay < 0:
            adjustedDelay = 0
            fpsActual = 1/(end-start)
        else:
            fpsActual = fps

        time.sleep(adjustedDelay)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

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


    return distance

#------------------------------------------------------------------------------------------
#Main Script
#------------------------------------------------------------------------------------------

depthPath = "navigation\kinect\KinectDepth_testData2.avi"
videoPath = "navigation\kinect\KinectRGB_testData2.avi"

depthStream = "http://192.168.1.100:8081/?action=stream"
videoStream = "http://192.168.1.100:8080/?action=stream"

fps = 80

processVideo(depthStream,videoStream,fps)




