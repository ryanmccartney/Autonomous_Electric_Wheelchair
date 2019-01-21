#NAME: kinectCalibrate.py
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

#Some Global Variables
vehicleLength = 0.45 #meters
vehicleWidth = 0.5 #meters
vehicleHeight = 1.35 #meters

unitDimensions = 0.1 #meters
kinectMaxRange = 3.2 #meters 

cameraAngle = 80 #degrees

mapLength = 40 #meters
mapWidth = 40 #meters
mapHeight = vehicleHeight*2

#Create Map
def createMap(name):

    mapPath = "navigation/map/"+name+".txt"

    #Define length and width
    lengthUnits = int(mapLength/unitDimensions)
    widthUnits = int(mapWidth/unitDimensions)
    Heightunits = int(2)

    #Create Empty Array
    map = np.zeros((Heightunits,lengthUnits,widthUnits), dtype=int)
    mapShape = map.shape
    mapLocation = np.true_divide(mapShape,2)
    mapLocation = mapLocation.astype(int)

    #Create the floor
    
    # Write the array to disk
    with open(mapPath, 'w') as outfile:
        
        outfile.write('# Saved Map. Map size is: {0}\n'.format(mapShape))

        for data_slice in map:  
            np.savetxt(outfile, data_slice, fmt='%-7.2f')
            outfile.write('# Next Slice\n')
    
    return mapShape, mapLocation

#Load the Map from file
def loadMap(name):

    mapPath = "navigation/map/"+name+".txt"

    # Read the map from disk
    map = np.loadtxt(mapPath)

    # Note that this returned a 2D array!

    #Recreating a 3D Array
    map = map.reshape(mapShape)

    return map

#Add frame to the map 
#def addMap(frame, distance, angle):


    #return mapLocation


#Optimised method for creating a graph
def createGrpah(data):
    
    width = len(data)
    height = 255+1
    size = (height,width)

    red = np.full(size,255,dtype=np.uint8)
    green = np.full(size,255,dtype=np.uint8)
    blue = np.full(size,255,dtype=np.uint8)
 
    #Populate Array with Data
    for w in range (0,width):
        
        red[data[w],w] = 209    
        green[data[w],w] = 66
        blue[data[w],w] = 244
    
    image = np.dstack((blue, green, red))
    return image

#Filter Image to Remove Noise
def applyFilter(image):
  
    #Gaussian
    #filteredFrame = cv.GaussianBlur(image,(5,5),0)

    #Average
    #kernel = np.ones((5,5),np.float32)/25
    #filteredFrame = cv.filter2D(image,-1,kernel)
        
    #Median
    filteredFrame = cv.medianBlur(image,5)

    #Bilateral Filtering
    #filteredFrame = cv.bilateralFilter(image,9,75,75)

    #No Filtering
    #filteredFrame = image
    
    return filteredFrame

#Processing Loop
def processVideo(depthPath,videoPath,fps):

    delay = 1/fps
    fpsActual = fps

    #Depth and Video Data
    depth = cv.VideoCapture(depthPath)
    video = cv.VideoCapture(videoPath)
 
    #Crosshair Size
    crosshairHeight = 10
    crosshairWidth = 10

    while(depth.isOpened()) and (video.isOpened()):

        start = time.time()

        ret, depthFrame = depth.read()
        ret, videoFrame = video.read()
        
        #Convert Matrix to Grayscale Image
        depthFrame = cv.cvtColor(depthFrame, cv.COLOR_BGR2GRAY)

        #Apply Filtering
        depthFrame = applyFilter(depthFrame)
     
        #Determine the Closest Point
        closestPoint = scanImage(depthFrame)
        distance = distanceCalc(closestPoint[0])

        #2D Graph the Area the Results
        mapData = scanStrip(depthFrame)
        graph = createGrpah(mapData)
        cv.imshow('Graph',graph)

        #Convert Depth Image Back to Colour Matrix
        depthFrame = cv.cvtColor(depthFrame,cv.COLOR_GRAY2RGB)

        #Add text with measurements
        font = cv.FONT_HERSHEY_SIMPLEX
        text = 'Closest point is %.2fm away.'%round(distance,2)
        cv.putText(videoFrame,text,(16,20), font, 0.6,(0,0,255),1,cv.LINE_AA)
        text = '%.2ffps'%round(fpsActual,2)
        cv.putText(videoFrame,text,(16,44), font, 0.6,(0,0,255),1,cv.LINE_AA)

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
        print("INFO: Processing duration for frame is %.2f seconds and the closest point is %.2f meters away." % (round((end-start),2), round(distance,2)))
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
    pointValue = 2048
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

#Optimised method for finding the closest point in each strip
@nb.jit(nopython=True)
def scanStrip(depthData):

    height = len(depthData)
    width = len(depthData[0])

    #Initialise with worst case
    outline = [2048] * width

    #Threshold for dealing with annomolies (reflective surfaces)
    threshold = 0

    #Populate Array with Data
    for w in range (0,width):
        
        for h in range (0,height):
      
            if  (depthData[h,w] <= outline[w]) and (depthData[h,w] >= threshold):
                outline[w] = depthData[h,w]

    return outline

#Returns infomraiton about how far away a point is in and image
def distanceCalc(depth):

    cameraAngle = 60

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

depthStream = "http://192.168.1.100:8081/?action=stream"
videoStream = "http://192.168.1.100:8080/?action=stream"
fps = 30

#Create Map
#start = time.time()
#mapShape, mapLocation = createMap("testMap")
#end = time.time()
#print("STATUS: Map creation took %.2f seconds." % round((end-start),2))

#Load Map      
#start = time.time()
#map = loadMap("testMap")
#end = time.time()
#print("STATUS: Loading the map took %.2f seconds." % round((end-start),2))

#print("INFO: The shape of the map is ",mapShape)
#print("INFO: The location in the map has been set as ",mapLocation)

processVideo(depthStream,videoStream,fps)




