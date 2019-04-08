#NAME:  buildMap.py
#DATE:  08/04/2019
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for aquiring depth data and building a 360 degree map
#COPY:  Copyright 2019, All Rights Reserved, Ryan McCartney

import cv2 as cv
import math
import time
import json
import numba as nb
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen
from control import Control

kinectWidthOfView = 64 #Degrees
kinectHeightOfView = 48 #Degrees
width = 640
height = 480
position = 240

#Logging Function (Pretty Console Output)
def log(logFilePath,entry):    

    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + entry

    #open a txt file to use for logging
    logFile = open(logFilePath,"a+")
    logFile.write(logEntry+"\n")
    logFile.close()
    print(logEntry)

#Returns infomraiton about how far away a point is in and image
def distanceCalc(depth):
    
    a = -0.0000000069
    b = 0.0000064344
    c = -0.0019066199
    d = 0.2331614352
    e = -9.4
    
    #Second Order Custom Estimation
    distance = (a*math.pow(depth,4))+(b*math.pow(depth,3))+(c*math.pow(depth,2))+(d*depth)+e

    #First Order Custom Estimation
    #m = 0.0161
    #c = -1.4698
    #distance = (m*depth)+c

    if distance < 0:
        distance = 0

    return distance

#Optimised method for finding the closest point in each strip 
#@nb.jit(nopython=True)
def scanStrip(depthImage):

    height = len(depthImage)
    width = len(depthImage[0])
    strip = [0] * width
    
    #Populate Array with Data
    for w in range (0,width):

        minPoint = 255
        for h in range (0,height):

            if minPoint > depthImage[h,w]:
                minPoint = depthImage[h,w]

        strip[w] = minPoint
        #strip[w] = depthImage[position,w]
    
    return strip

#Translate to X/Y coordinates
def translate(depthData):

    dataPoints = len(depthData)
    deltaTheta = math.radians(kinectWidthOfView/dataPoints)
    theta = -math.radians(kinectWidthOfView/2)

    xPoints = [0] * dataPoints
    yPoints = [0] * dataPoints

    for n in range (0,dataPoints):         
        d = distanceCalc(depthData[n])
        xPoints[n] = d*math.sin(theta)
        yPoints[n] = d*math.cos(theta)
        theta = theta + deltaTheta
    log(logFilePath,"INFO = "+str(dataPoints)+" points translated.")
    return xPoints,yPoints

def rotate(xValues,yValues,angle):
    #Invert Angle
    angle = -angle
    #Number of Points
    points = len(xValues)
    #Initialise Arrays
    xValuesRotated = [0] * points
    yValuesRotated = [0] * points

    if len(xValues) == len(yValues):       
        for i in range (0,points):
            xValuesRotated[i] = (xValues[i]*math.cos(math.radians(angle)))-(yValues[i]*math.sin(math.radians(angle)))
            yValuesRotated[i] = (yValues[i]*math.cos(math.radians(angle)))+(xValues[i]*math.sin(math.radians(angle)))
        log(logFilePath,"INFO = Points rotated "+str(-angle)+" degrees.")
    else:
        log(logFilePath,"ERROR = Input Arrays Mismatched, length of X is not the same as length of Y.")

    return xValuesRotated, yValuesRotated

try:
    #Open Configuration File
    configurationFile = open('testing/XYtranslations/settings.json').read()
    configuration = json.loads(configurationFile)

    #Get the details of the log file from the configuration
    logFilePath = configuration['general']['logFile']
    depthStreamURL = configuration['streams']['kinectDepth']['url']
    imageStreamURL = configuration['streams']['kinectRGB']['url']

    #open a txt file to use for logging and clear it
    logFile = open(logFilePath,"w")
    logFile.close()

    log(logFilePath,"INFO = Main Thread has accessed log file.")

except:
    log(logFilePath,"ERROR = Log file could not be created.")
    exit()

#Initialise Control Class
try:
    wheelchair = Control(configuration)

    try:
        #Start Sequence
        log(logFilePath,"INFO = Starting Mapping Sequence.")

        #Some Setup
        angleIncrement = 45
        readPoints = int(360/angleIncrement)

        #Create plot
        plt.ion()
        fig = plt.figure()
              
        while 1:

            #Setup Plot
            ax = fig.add_subplot(1, 1, 1, facecolor="1.0")
            plt.xlim(-3.2,3.2)
            plt.ylim(-3.2,3.2)
            ax.scatter(0, 0, s=10, c='r', marker="s", label='Wheelchair Position')
            plt.draw()

            #Decorate Graph
            plt.title('2D Floor Plane Map of Enviroment')
            plt.legend(loc=2)
            plt.xlabel('x (m)')
            plt.ylabel('y (m)')
            
            currentAngleOfRoation = 0

            for i in range (0,readPoints):

                #Get a Depth Image
                request = urlopen(depthStreamURL, timeout=1)
                array = np.asarray(bytearray(request.read()), dtype="uint8")
                depthFrame = cv.imdecode(array,-1)

                #Get an RGB Image
                request = urlopen(imageStreamURL, timeout=1)
                array = np.asarray(bytearray(request.read()), dtype="uint8")
                imageFrame = cv.imdecode(array,-1)

                #Convert Depth Frame to Grayscale
                #depthFrame = cv.cvtColor(depthFrame,cv.COLOR_BGR2GRAY)

                #Image Resize
                imageFrame = cv.resize(imageFrame,(width,height))
                depthFrame = cv.resize(depthFrame,(width,height))

                #Scan Image for 2D Profile
                depthData = scanStrip(depthFrame)

                #Translate 2D Profile to XY
                xPoints,yPoints = translate(depthData)

                #Rotate Values
                xPointsRotated, yPointsRotated = rotate(xPoints,yPoints,currentAngleOfRoation)

                #Show the frame
                cv.imshow('Current Image Frame',imageFrame)  
                cv.imshow('Current Depth Frame',depthFrame) 
                
                #Plot Data
                ax.scatter(xPointsRotated, yPointsRotated, s=10, c=np.random.rand(3,), marker="s")
                                
                #Add Wheelchair Location
                ax.scatter(0, 0, s=10, c='r', marker="s")
                fig.canvas.draw_idle()
                plt.show()
                plt.pause(0.5)

                wheelchair.turn(angleIncrement)
                currentAngleOfRoation = currentAngleOfRoation + angleIncrement 
                time.sleep(0.5)
                log(logFilePath,"INFO = "+str(currentAngleOfRoation)+" degree phase Completed.")

            #Move on when any key is pressed
            log(logFilePath,"INFO = 360 Degree Rotation Complete.")
            log(logFilePath,"ACTION = Press any key to continue.")
            cv.waitKey()
            fig.clf()

    except:
        log(logFilePath,"ERROR = Could not start mapping.")
        log(logFilePath,"STATUS = Terminating Program.")
        exit()

except:
    log(logFilePath,"ERROR = Could not initiate Control class.")
    log(logFilePath,"STATUS = Terminating Program.")
    exit()