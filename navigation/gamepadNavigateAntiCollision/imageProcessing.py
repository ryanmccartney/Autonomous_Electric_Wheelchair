#NAME:  imageProcessing.py
#DATE:  08/02/2019
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for aquiring and processing image data from network streams
#COPY:  Copyright 2019, All Rights Reserved, Ryan McCartney

import threading
import numpy as np
import cv2 as cv
import time
import imutils
import numba as nb
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from streamCapture import StreamCapture
import time
import math

#define threading wrapper
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class imageProcessing:

    debug = False
    processing = False
    
    def __init__(self,configuration):
        
        #load the configuratio
        try:
            configuration = configuration
            currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
            logEntry = currentDateTime + ": " + "INFO = The configuration file has been accessed." + "\n"
            print(logEntry)
        except:
            currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
            logEntry = currentDateTime + ": " + "ERROR = The configuration file cannot be accessed." + "\n"
            print(logEntry)

        #Load Configuration Variables
        try:
            self.kinectDepth_url = configuration['streams']['kinectDepth']['url']
            self.kinectDepth_name = configuration['streams']['kinectDepth']['name']
            self.kinectImage_url = configuration['streams']['kinectRGB']['url']
            self.kinectImage_name = configuration['streams']['kinectRGB']['name']
            self.webcam_url = configuration['streams']['webcam']['url']
            self.webcam_url = configuration['streams']['webcam']['name']

            self.fps = configuration['general']['fps']
            self.kinectAngle = configuration['general']['kinectAngle']
            self.scaleFactor = configuration['general']['scaleFactor']

            self.mapUnits = configuration['map']['unitSize']
            self.mapLength = configuration['map']['length']
            self.mapWidth = configuration['map']['width']
            self.mapHeight = configuration['map']['height']
            
            self.vehicleLength = configuration['vehicle']['length']
            self.vehicleWidth = configuration['vehicle']['width']
            self.vehicleHeight = configuration['vehicle']['height']

            #Get the details of the log file from the configuration
            logFilePath = configuration['general']['logFileDirectory']
            logFileName = configuration['general']['logFileName']
            logFileFullPath = logFilePath + logFileName

            
        except:
            currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
            logEntry = currentDateTime + ": " + "ERROR = The configuration file cannot be decoded." + "\n"
            print(logEntry)
     
        #Open the log file
        try:
            #open a txt file to use for logging 
            self.logFile = open(logFileFullPath,"a+")
            currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
            logEntry = currentDateTime + ": " + "INFO = Log file accessed by Image Proccessor." + "\n"
            self.logFile.write(logEntry)
            print(logEntry)
        except:
            currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
            logEntry = currentDateTime + ": " + "ERROR: Unable to access log file when staring image processing." + "\n"
            print(logEntry)

        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "STATUS = Image Processing Initiaited." + "\n"
        self.logFile.write(logEntry)
        print(logEntry)

    #Create Map
    def createMap(self, name):
        
        #Write Log Entry
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "INFO = Generating the Map." + "\n"
        self.logFile.write(logEntry)
        print(logEntry)

        mapPath = "navigation/map/"+name+".txt"

        #Define length and width
        lengthUnits = int(self.mapLength/self.mapUnits)
        widthUnits = int(self.mapWidth/self.mapUnits)
        heightunits = int(self.mapHeight/self.mapUnits)

        #Create Empty Array
        map = np.zeros((heightunits,lengthUnits,widthUnits), dtype=int)
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

        #Write Log Entry
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "STATUS = Map has been sucessfully generated." + "\n"
        self.logFile.write(logEntry)
        print(logEntry)

        return mapShape, mapLocation

    #Load the Map from file
    def loadMap(self, name, mapShape):

        #Write Log Entry
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "INFO = Loading map from file..." + "\n"
        self.logFile.write(logEntry)
        print(logEntry)

        mapPath = "navigation/map/"+name+".txt"

        #Read the map from disk
        map = np.loadtxt(mapPath)

        #Recreating a 3D Array
        map = map.reshape(mapShape)

        #Write Log Entry
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "STATUS = Map has been sucessfully loaded." + "\n"
        self.logFile.write(logEntry)
        print(logEntry)

        return map

    #Convert depth image to a floor plan view
    def createFloorPlan(self,depthImage):

        width = len()
        height = 255+1
        size = (height,width)

        red = np.full(size,255,dtype=np.uint8)
        green = np.full(size,255,dtype=np.uint8)
        blue = np.full(size,255,dtype=np.uint8)

    #Optimised method for creating a graph
    def createGrpah(self,data):
    
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

        #Create a single image with the channels
        image = np.dstack((blue, green, red))

        return image

    #Filter Image to Remove Noise
    def applyFilter(self,filter,image):
        
        #Gaussian
        if filter == 1:
            filteredFrame = cv.GaussianBlur(image,(5,5),0)
        #Average
        elif filter == 2:
            kernel = np.ones((5,5),np.float32)/25
            filteredFrame = cv.filter2D(image,-1,kernel)
        #Median
        elif filter == 3:
            filteredFrame = cv.medianBlur(image,5)
        #Bilateral Filtering
        elif filter == 4:
            filteredFrame = cv.bilateralFilter(image,9,75,75)
        #No Filtering
        else:
            filteredFrame = image
    
        return filteredFrame

    #Processing Loop
    @threaded
    def processStream(self):

        delay = 1/self.fps
        fpsActual = self.fps
        
        #Crosshair Size
        crosshairHeight = 10
        crosshairWidth = 10

        try:
            depth = StreamCapture(self.kinectDepth_url,self.kinectDepth_name)
            video = StreamCapture(self.kinectImage_url,self.kinectImage_name)
            depth.displayStream = True
            video.displayStream = True

            #Get an initial Frame
            depthFrame = depth.getFrame()
            videoFrame = video.getFrame()

            #Get Depth Frame Dimensions
            height = depthFrame.shape[0]
            width = depthFrame.shape[1]

            #Reduce Depth Image Resolution
            mappedHeight = int(height*self.scaleFactor)
            mappedWidth = int(width*self.scaleFactor)

            #Write Log Entry
            currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
            logEntry = currentDateTime + ": " + "INFO = Starting processing on data streams." + "\n"
            self.logFile.write(logEntry)
            print(logEntry)

            while (video.stream == True) and (depth.stream == True):

                start = time.time()

                #Get Latest Frames
                depthFrame = depth.frame
                videoFrame = video.frame

                #Convert Matrix to Grayscale Image
                depthFrame = cv.cvtColor(depthFrame, cv.COLOR_BGR2GRAY)

                #Apply Filtering
                depthFrame = self.applyFilter(0,depthFrame)

                #Reduce Resolution of Kinetic Depth to a Managable Size
                #depthFrame = cv.resize(depthFrame, (mappedWidth, mappedHeight), interpolation = cv.INTER_CUBIC)   

                #Determine the Closest Point
                closestPoint = self.scanImage(depthFrame)
                self.closestObject = self.distanceCalc(closestPoint[0])

                #2D Graph the Area the Results
                mapData = self.scanStrip(depthFrame)
                graph = self.createGrpah(mapData)
                cv.imshow('Graph',graph)

                #Convert Depth Image Back to Colour Matrix
                depthFrame = cv.cvtColor(depthFrame,cv.COLOR_GRAY2RGB)

                #Add text with measurements
                font = cv.FONT_HERSHEY_SIMPLEX
                text = 'Closest point is %.2fm away.'%round(self.closestObject,2)
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
                cv.imshow(self.kinectDepth_name,depthFrame)
                cv.imshow(self.kinectImage_name,videoFrame)

                end = time.time()

                if self.debug == True:
                    print("INFO: Processing duration for frame is %.2f seconds and the closest point is %.2f meters away." % (round((end-start),2), round(self.closestObject,2)))
                
                adjustedDelay = delay-(end-start)

                if adjustedDelay < 0:
                    adjustedDelay = 0
                    fpsActual = 1/(end-start)
                else:
                    fpsActual = self.fps

                time.sleep(adjustedDelay)
                self.processing = True

                if cv.waitKey(1) & 0xFF == ord('q'):
                    break

            self.processing = False
            depth.stream = False
            video.stream = False
            cv.destroyAllWindows()

        except:
            #Write Log Entry
            currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
            logEntry = currentDateTime + ": " + "ERROR = Could not access video streams." + "\n"
            self.logFile.write(logEntry)
            print(logEntry)

    #Optimised method for finding the closest point in an image
    @staticmethod
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
    @staticmethod
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
    def distanceCalc(self,depth):

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
        kinectAngleRads = math.radians(self.kinectAngle)
        groundDistance = math.sin(kinectAngleRads)*distance
        groundDistance = groundDistance - self.vehicleLength
    
        return groundDistance
