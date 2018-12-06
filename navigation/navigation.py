#NAME:  mapDepth.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for mapping depth data in 3D from a grayscale image
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

import threading
import numpy as np
import cv2 as cv
import imutils
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from cameraData import cameraData
import time
import numba as nb
import timeit

#define threading wrapper
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class Navigation:

    scaleFactor = 1
    closestDistance = 255
    fps = 30

    def __init__(self,unitSize,mapLength,mapWidth,mapHieght):

        #Determine matrix for map's size
        self.mapLengthUnits = mapLength/unitSize
        self.mapWidthUnits = mapWidth/unitSize
        self.mapHieghtUnits = mapHieght/unitSize

        #Cast to integars
        self.mapLengthUnits = int(self.mapLengthUnits)
        self.mapWidthUnits = int(self.mapWidthUnits)
        self.mapHieghtUnits = int(self.mapHieghtUnits)
        
    
    #Optimised method for plotting a point point cloud in a matrix
    @staticmethod
    @nb.jit(nopython=True)
    def populateMatrix(image):

        height = image.shape[0]
        width = image.shape[1]

        pointCloud = np.empty((height,width,256))
    
        #Populate Array with Data
        for x in range (0,height):

            for y in range (0,width):

                z = image[x,y]
                pointCloud[x,y,z] = 1
                    
        return pointCloud
    
    def createPointCloud(self,frame):
        
        height = frame.shape[0]
        width = frame.shape[1]

        mappedHeight = int(height/self.scaleFactor)
        mappedWidth = int(width/self.scaleFactor)
        
        #Ensure image is grayscale for depth values
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        #Reduce Resolution of Kinetic Depth to a Managable Size
        resizedFrame = cv.resize(frame, (mappedWidth, mappedHeight), interpolation = cv.INTER_CUBIC)
        
        pointCloud = self.populateMatrix(resizedFrame)
 
        return pointCloud

    #Optimised method for finding the closest point in an image
    @staticmethod
    @nb.jit(nopython=True)
    def scanImage(image):

        height = image.shape[0]
        width = image.shape[1]

        #Initialise with worst case
        pointValue = 0
        pointHeight = 0
        pointWidth = 0
        
        #Populate Array with Data
        for h in range (0,height):

            for w in range (0,width):

                if  image[h,w] >= pointValue:
                    pointValue = image[h,w]
                    pointHeight = h
                    pointWidth = w
                    
        results = [pointValue, pointWidth, pointHeight]
       
        return results

    #Closest point main function for collision avoidance.
    @threaded
    def closestPoint(self,streamURL,showStream):
        
        #Caculate Delay to prevent unneccesary processing
        delay = 1/self.fps
        name = "Closest Point in Path Detection"

        depth = cameraData(streamURL,name)
        frame = depth.getFrame()

        #Get Height and Width in Pixels of the Frame
        height = frame.shape[0]
        width = frame.shape[1]

        #Reduced Resolution
        mappedHeight = int(height/self.scaleFactor)
        mappedWidth = int(width/self.scaleFactor)

        cropPathWidth = int(200/self.scaleFactor)
        cropPathHeight = int(300/self.scaleFactor)

        x1 = int((mappedWidth/2) - (cropPathWidth/2))
        x2 = int(x1 + cropPathWidth)

        y1 = int(mappedHeight-cropPathHeight)
        y2 = int(mappedHeight)

        pathWidth = int(cropPathWidth*self.scaleFactor)
        pathHeight = int(cropPathHeight*self.scaleFactor)

        topW = int((width/2) - (pathWidth/2))
        topH = int(height - pathHeight)

        bottomW = int((width/2) + (pathWidth/2))
        bottomH = int(height)

        while 1:
            
            frame = depth.getFrame()

            #Ensure image is grayscale
            frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            #Blur Image
            frame = cv.GaussianBlur(frame,(5,5),0)

            #Reduce Resolution of Kinetic Depth to a Managable Size
            resizedFrame = cv.resize(frame, (mappedWidth, mappedHeight), interpolation = cv.INTER_CUBIC)
            frame = cv.resize(resizedFrame, (width, height), interpolation = cv.INTER_CUBIC)
            resizedFrame = resizedFrame[y1:y2, x1:x2]

            #Scan Pixel by Pixel for Closest Point
            closestPoint = self.scanImage(resizedFrame)
            self.closestDistance = closestPoint[0]
            
            #Set Max Speed with this reading
            self.maxSpeed = self.calcMaxSpeed(self.closestDistance)

            if showStream == True:

                #Convert Back to Colour
                frame = cv.cvtColor(frame,cv.COLOR_GRAY2RGB) 
                
                #Map Width and Height back to normal
                closestPoint[1] = int(topW + (closestPoint[1]*self.scaleFactor))
                closestPoint[2] = int(topH + (closestPoint[2]*self.scaleFactor))

                #Crosshair Calculations
                crosshairRatio = int(25/self.scaleFactor)
                crosshairHeight = int(mappedHeight/crosshairRatio)
                crosshairWidth = int(mappedWidth/crosshairRatio)
                
                #Horizontal Line
                cv.line(frame,((closestPoint[1]-crosshairWidth),closestPoint[2]),((closestPoint[1]+crosshairWidth),closestPoint[2]),(0,0,255),2)
                #Vertical Line
                cv.line(frame,(closestPoint[1],(closestPoint[2]-crosshairHeight)),(closestPoint[1],(closestPoint[2]+crosshairHeight)),(0,0,255),2)
                #Path Rectangle
                cv.rectangle(frame,(topW,topH),(bottomW,bottomH),(0,255,0),2)

                #Add text with details
                font = cv.FONT_HERSHEY_SIMPLEX
                text = 'Closest Point is ' + str(self.closestDistance) +'m away.'
                cv.putText(frame,text,(topW,(topH-5)), font, 0.4,(0,0,255),1,cv.LINE_AA)

                cv.imshow(name,frame)

                #Quit program when 'esc' key is pressed
                k = cv.waitKey(5) & 0xFF
                if k == 27:
                    break

            time.sleep(delay)
    
    @threaded
    def plotPointCloud(self,pointCloud):

        # Data for three-dimensional scattered points
        z,x,y = pointCloud.nonzero()

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, -y, -z, zdir='z', c= 'blue')
        #ax.view_init(60, 35)

        #Label Map
        ax.set_xlabel('Length Units')
        ax.set_ylabel('Width Units')
        ax.set_zlabel('Hieght Units')

        
        #Create a file for each frame depending on time
        currentDateTime = time.strftime("%d%m%Y-%H%M%S")
        filename = "data\pointCloudPlots\Point Cloud Plot -" + currentDateTime + ".png"
        plt.savefig(filename)

        print("STATUS: 3D Point Cloud Plotted")
   
    @threaded
    def writeCSV(self,pointCloud):

        arrayDimensions = pointCloud.shape

        #Create a file for each frame depending on time
        currentDateTime = time.strftime("%d%m%Y-%H%M%S")
        filename = "data\pointCloudData\Point Cloud Data -" + currentDateTime + ".csv"

        #create a CSV file for the frame data 
        pointCloudFile = open(filename,"w+")
        dataEntry = "X,Y,Z\n"
        pointCloudFile.write(dataEntry)

        print("INFO: The dimensions of the inputted array are ",arrayDimensions)

        #Write data into CSV file
        for x in range (0,arrayDimensions[0]):

            for y in range (0,arrayDimensions[1]):

                for z in range (0,arrayDimensions[2]):

                    if pointCloud[x,y,z] != 0:
                        
                        #create a data entry
                        dataEntry = str(x) + "," + str(y) + "," + str(z) + "\n"
                        pointCloudFile.write(dataEntry)
        
        pointCloudFile.close()