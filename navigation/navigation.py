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
    fps = 40

    def __init__(self,unitSize,mapLength,mapWidth,mapHieght):

        #Determine matrix for map's size
        self.mapLengthUnits = mapLength/unitSize
        self.mapWidthUnits = mapWidth/unitSize
        self.mapHieghtUnits = mapHieght/unitSize

        #Cast to integars
        self.mapLengthUnits = int(self.mapLengthUnits)
        self.mapWidthUnits = int(self.mapWidthUnits)
        self.mapHieghtUnits = int(self.mapHieghtUnits)
        
    def mapFrame(self,frame):
        
        height = frame.shape[0]
        width = frame.shape[1]

        mappedHeight = int(height/self.scaleFactor)
        mappedWidth = int(width/self.scaleFactor)
        
        #Ensure image is grayscale
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        #Reduce Resolution of Kinetic Depth to a Managable Size
        resizedFrame = cv.resize(frame, (mappedWidth, mappedHeight), interpolation = cv.INTER_CUBIC)
        
        #Create 3D Array of Curent View
        mappedDepth = np.zeros((mappedHeight,mappedWidth,256))
        
        file = open("processingTimePython.csv","a")
        start = time.time()

        #Populate Array with Data
        for h in range (0,mappedHeight):

            for w in range (0,mappedWidth):

                depth = int(resizedFrame[h,w])
                mappedDepth[h,w,depth] = 1

        end = time.time()
        processingTime = (end-start)*1000
        fileData = str(mappedHeight) + "," + str(mappedWidth) + "," + str(processingTime) + "\n"
        print(fileData)
        file.write(fileData)
        file.close() 
 
        return mappedDepth

    @staticmethod
    @nb.jit(nopython=True)
    def scanImage(image):

        height = image.shape[0]
        width = image.shape[1]

        #Initialise with worst case
        pointValue = 255
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

        while 1:
            
            frame = depth.getFrame()

            #Ensure image is grayscale
            frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            #Reduce Resolution of Kinetic Depth to a Managable Size
            resizedFrame = cv.resize(frame, (mappedWidth, mappedHeight), interpolation = cv.INTER_CUBIC)
            frame = cv.resize(resizedFrame, (width, height), interpolation = cv.INTER_CUBIC)


            #Scan Pixel by Pixel for Closest Point
            closestPoint = self.scanImage(resizedFrame)
            self.closestDistance = closestPoint[0]
            
            if showStream == True:

                #Convert Back to Colour
                frame = cv.cvtColor(frame,cv.COLOR_GRAY2RGB) 

                #Crosshair Calculations
                crosshariRatio = 25
                crosshairHeight = int(mappedHeight/crosshariRatio)
                crosshairWidth = int(mappedWidth/crosshariRatio)
                
                #Horizontal Line
                cv.line(frame,((closestPoint[1]-crosshairWidth),closestPoint[2]),((closestPoint[1]+crosshairWidth),closestPoint[2]),(0,0,255),2)
                #Vertical Line
                cv.line(frame,(closestPoint[1],(closestPoint[2]-crosshairHeight)),(closestPoint[1],(closestPoint[2]+crosshairHeight)),(0,0,255),2)
            
                cv.imshow(name,frame)

                #Quit program when 'esc' key is pressed
                k = cv.waitKey(5) & 0xFF
                if k == 27:
                    break

            time.sleep(delay)
    
  
    def plotPointCloud(self,mappedArray):

        # Data for three-dimensional scattered points
        z,x,y = mappedArray.nonzero()

        print("STATUS: Plotting 3D Graph")

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, zdir='z', c= 'blue')
        #ax.view_init(60, 35)

        #Label Map
        ax.set_xlabel('Length Units')
        ax.set_ylabel('Width Units')
        ax.set_zlabel('Hieght Units')

        plt.savefig('navigation\map.png')

        print("STATUS: 3D Point Cloud Plotted")

    @threaded
    def writeCSV(self,mappedArray):

        arrayDimensions = mappedArray.shape
        print("INFO: The dimensions of the inputted array are ",arrayDimensions)

        with open('navigation\pointCloud.csv', mode='w') as pointCloud:

            writePoints = csv.writer(pointCloud, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writePoints.writerow(['X', 'Y', 'Z'])

            for x in range (0,):

                for y in range (0,self.width):

                    for z in range (0,255):

                        if mappedArray != 0:

                            writePoints.writerow([x, y, z])
