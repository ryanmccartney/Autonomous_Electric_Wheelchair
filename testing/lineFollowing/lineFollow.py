
#NAME: guiExample.py
#DATE: 08/02/2019
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python function for navigating the wheelchair with an XBOX 360 game controller avoiding obstacles
#COPY: Copyright 2019, All Rights Reserved, Ryan McCartney

from control import Control
import cv2 as cv
import tkinter as tk
import numpy as np
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

def processImage(image):

    crosshair = 20

    #Convert Matrix to Grayscale Image
    grayscaleImage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Gaussian blur
    blurImage = cv.GaussianBlur(grayscaleImage,(5,5),0)

    # Color thresholding
    ret,thresholdImage = cv.threshold(blurImage,60,255,cv.THRESH_BINARY_INV)

    #Erode and dilate to remove accidental line detections
    mask = cv.erode(thresholdImage, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)

    #Find the contours of the frame
    _, contours, hierarchy = cv.findContours(mask, 1, cv.CHAIN_APPROX_NONE)
    
    #Find the biggest contour (if detected)
    if len(contours) > 0:

        contourMax = max(contours, key=cv.contourArea)
        coutourMoment = cv.moments(contourMax)

        contourXPos = int(coutourMoment['m10']/coutourMoment['m00'])
        contourYPos = int(coutourMoment['m01']/coutourMoment['m00'])
        contourPosition = [contourXPos,contourYPos]

        cv.line(image,(contourXPos,(contourYPos-crosshair)),(contourXPos,(contourYPos+crosshair)),(0,0,255),2)
        cv.line(image,((contourXPos-crosshair),contourYPos),((contourXPos+crosshair),contourYPos),(0,0,255),2)
        cv.drawContours(image, contours, -1, (255,0,0), 1)
    
    else:
        contourPosition = 0

    return image,contourPosition

def addGoal(image):
    
    buffer = 0.2

    #Determine Image Size
    width = frame.shape[1] 
    height = frame.shape[0]

    #Determine Goal Location
    goalWidth = int(width*buffer)
    goalHeight = int(height*buffer)
    xL = int((width/2)-(goalWidth/2))
    xR = int((width/2)+(goalWidth/2))
    yT = int((height/2)-(goalHeight/2))
    yB = int((height/2)+(goalHeight/2))

    #Left & Right Line
    cv.line(image,(xL,0),(xL,height),(0,255,0),2)
    cv.line(image,(xR,0),(xR,height),(0,255,0),2)

    #Top and Bottom Line
    cv.line(image,(0,yT),(width,yT),(0,255,0),2)
    cv.line(image,(0,yB),(width,yB),(0,255,0),2)

    goalArea = [xL,yB,xR,yT]

    return image,goalArea

def follow(image,contourCenter,goalArea):

    maxSpeed = 40
    minSpeed = 0
    maxAngle = 50
    minAngle = -50
    crosshair = 20 
    command = "RUN"

    #Determine Image Size
    width = frame.shape[1] 
    height = frame.shape[0]

    #Contour Position
    contourX = contourCenter[0]
    contourY = contourCenter[1]

    #Goal Coordinates
    goalLeftX = goalArea[0]
    goalRightX = goalArea[2]
    goalTopY = goalArea[3]
    goalBottomY = goalArea[1]

    #Determine Steering Angle
    if (contourX > goalLeftX) and (contourX < goalRightX):
        angle = 0
        cv.line(image,(contourX,(contourY-crosshair)),(contourX,(contourY+crosshair)),(0,255,0),2)
    elif contourX < goalLeftX:
        angleFactor = (goalLeftX-contourX)/(goalLeftX)
        angle = int(minAngle*angleFactor)
    elif contourX > goalRightX: 
        angleFactor = (contourX-goalRightX)/(width-goalRightX)
        angle = int(maxAngle*angleFactor)
    else:
        speed = 0

    #Determine Speed based on Y position of Goal
    if (contourY > goalTopY) and (contourY < goalBottomY):
        speed = 40
        cv.line(image,((contourX-crosshair),contourY),((contourX+crosshair),contourY),(0,255,0),2)
    elif contourY < goalBottomY:
        speed = 20
    elif contourY > goalTopY:
        speed = 20
    else:
        speed = 0

    log(logFilePath,"INFO = Speed adjusted to "+str(speed)+". Angle adjusted to "+str(angle)+".")
    #wheelchair.transmitCommand(speed,angle,command)

#Get the details of the log file from the configuration
logFilePath = "data/logs/lineFollowingTest.txt"

#open a txt file to use for logging and clear it
logFile = open(logFilePath,"w")
logFile.close()

log(logFilePath,"INFO = Line following test sequence starting.")

# Load an color image in grayscale
frame = cv.imread('testing/lineFollowing/line3.jpg',cv.IMREAD_COLOR)

#Show the frame
cv.imshow('Original Image',frame)  
    
frame,contourPosition = processImage(frame)
frame,goalArea = addGoal(frame)
follow(frame,contourPosition,goalArea)

log(logFilePath,"INFO = Image Processed")

#Show the frame
cv.imshow('Processed Image',frame)  

# quit program when 'esc' key is pressed
cv.waitKey()