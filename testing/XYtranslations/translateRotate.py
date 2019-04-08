#NAME:  translateRotate.py
#DATE:  08/02/2019
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A series of python methods for rotate cartesian coordinates in a map
#COPY:  Copyright 2019, All Rights Reserved, Ryan McCartney

import cv2 as cv
import math
import numba as nb
import numpy as np
import matplotlib.pyplot as plt

kinectWidthOfView = 64 #Degrees
kinectHeightOfView = 48 #Degrees
width = 640
height = 480
position = 200

#Returns infomraiton about how far away a point is in and image
def distanceCalc(depth):

    #First Order Custom Estimation
    m = 0.0161
    c = -1.4698
    distance = (m*depth)+c

    if distance < 0:
        distance = 0

    return distance

#Optimised method for finding the closest point in each strip 
@nb.jit(nopython=True)
def scanStrip(depthImage):

    height = len(depthImage)
    width = len(depthImage[0])
    strip = [0] * width
    
    #Populate Array with Data
    for w in range (0,width):

        strip[w] = depthImage[position,w]
    
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
    else:
        print("ERROR: Input Arrays Mismatched, length of X is not the same as length of Y.")
    
    return xValuesRotated, yValuesRotated

#Image Locations
imagePath = 'testing/XYtranslations/Image.jpg'
depthPath = 'testing/XYtranslations/Depth.jpg'

#Image Read
imageFrame = cv.imread(imagePath,cv.IMREAD_COLOR)
depthFrame = cv.imread(depthPath,cv.IMREAD_COLOR)

#Convert Depth Frame to Grayscale
depthFrame = cv.cvtColor(depthFrame,cv.COLOR_BGR2GRAY)

#Image Resize
imageFrame = cv.resize(imageFrame,(width,height))
depthFrame = cv.resize(depthFrame,(width,height))

#Scan Image for 2D Profile
depthData = scanStrip(depthFrame)

#Translate 2D Profile to XY
xPoints,yPoints = translate(depthData)

#Rotate Values
xPointsRotated, yPointsRotated = rotate(xPoints,yPoints,90)

#Show the frame
cv.imshow('Image Frame',imageFrame)  
cv.imshow('Depth Frame',depthFrame) 

# Create plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, facecolor="1.0")

#Plot Data
ax.scatter(xPoints, yPoints, s=10, c='b', marker="s", label='Map')
ax.scatter(xPointsRotated, yPointsRotated, s=10, c='g', marker="s", label='Map Rotated 90 Degreees Clockwise')
ax.scatter(0, 0, s=10, c='r', marker="s", label='Wheelchair Position')
plt.title('2D Map of Enviroment')
plt.legend(loc=2)
plt.xlabel('x')
plt.ylabel('y')
plt.show()

#Move on when any key is pressed
cv.waitKey()