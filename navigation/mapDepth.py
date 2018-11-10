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

class mapDepth:

    height = 640
    width = 640
    closest = 255

    def __init__(self,unitSize,mapLength,mapWidth,mapHieght):

        #Determine matrix for map's size
        self.mapLengthUnits = mapLength/unitSize
        self.mapWidthUnits = mapWidth/unitSize
        self.mapHieghtUnits = mapHieght/unitSize

        #Cast to integars
        self.mapLengthUnits = int(self.mapLengthUnits)
        self.mapWidthUnits = int(self.mapWidthUnits)
        self.mapHieghtUnits = int(self.mapHieghtUnits)
        
    def readFrameSize(self,frame):

        #Find it's Width and Hieght 
        self.height = np.size(frame, 0)
        self.width = np.size(frame, 1)

        #Print some information
        print("INFO: The width of the depth image is ",self.width," and its height is ",self.height)

    def mapFrame(self,frame):

        factor = 15
        mapped_height = int(self.height/factor)
        mapped_width = int(self.width/factor)
        
        #Ensure image is grayscale
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        #Reduce Resolution of Kinetic Depth to a Managable Size
        resizedFrame = cv.resize(frame, (mapped_width, mapped_height), interpolation = cv.INTER_CUBIC)
        
        #Create 3D Array of Curent View
        mappedDepth = np.zeros((mapped_height,mapped_width,256))
        
        file = open("processingTimePython.csv","a")
        start = time.time()

        #Populate Array with Data
        for h in range (0,mapped_height):

            for w in range (0,mapped_width):

                depth = int(resizedFrame[h,w])
                mappedDepth[h,w,depth] = 1

        end = time.time()
        processingTime = (end-start)*1000
        fileData = str(mapped_height) + "," + str(mapped_width) + "," + str(processingTime) + "\n"
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
        distance = 255
        
        #Populate Array with Data
        for h in range (0,height):

            for w in range (0,width):

                if  distance < image[h,w]:
                    distance = image[h,w]
                
        return distance

    def closestPoint(self,frame):
       
        factor = 1
        mapped_height = int(self.height/factor)
        mapped_width = int(self.width/factor)
        
        #Ensure image is grayscale
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        #Reduce Resolution of Kinetic Depth to a Managable Size
        resizedFrame = cv.resize(frame, (mapped_width, mapped_height), interpolation = cv.INTER_CUBIC)

        #Open file to record timing results     
        file = open("processingTimeNumba.csv","a")
        
        #Time processing of the image
        start = time.time()
        self.closest = self.scanImage(resizedFrame)
        end = time.time()
        
        #Calculate time and write to file
        processingTime = (end-start)
        fileData = str(mapped_height) + "," + str(mapped_width) + "," + str(processingTime) + "\n"
        print(fileData)
        file.write(fileData)
        file.close() 
  
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