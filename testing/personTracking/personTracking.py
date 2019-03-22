#NAME:  personTracking.py
#DATE:  08/02/2019
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for tracking people data streamed from a kinect camera
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

import threading
import numpy as np
import cv2 as cv
import time
import math
import imutils
from datetime import datetime
from imutils.object_detection import non_max_suppression
from control import Control
from imutils import paths

#define threading wrapper
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class PersonTracking:

    frameWidth = 640
          
    def __init__(self,configuration):
        
        #Load Configuration Variables
        try:
            self.kinectDepth_url = configuration['streams']['kinectDepth']['url']
            self.kinectDepth_name = configuration['streams']['kinectDepth']['name']
            self.kinectImage_url = configuration['streams']['kinectRGB']['url']
            self.kinectImage_name = configuration['streams']['kinectRGB']['name']
            self.webcam_url = configuration['streams']['webcam']['url']
            self.webcam_url = configuration['streams']['webcam']['name']

            self.fps = configuration['general']['fps']
            self.maxSpeed = configuration['control']['maxSpeed']
            self.minAngle = configuration['control']['minAngle']
            self.maxAngle = configuration['control']['maxAngle']

            #Get the details of the log file from the configuration
            logFilePath = configuration['general']['logFileDirectory']
            logFileName = configuration['general']['logFileName']
            logFileFullPath = logFilePath + logFileName
      
        except:
            currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
            logEntry = currentDateTime + ": " + "ERROR = The configuration file cannot be decoded." + "\n"
            print(logEntry)
        
        #Try Initialising the control class
        try:
            self.wheelchair = Control(configuration)

            currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
            logEntry = currentDateTime + ": " + "INFO = Control Established." + "\n"
            print(logEntry)
        
        except:
            currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
            logEntry = currentDateTime + ": " + "ERROR = Cotrol Class could not be initiated." + "\n"
            print(logEntry)
    
        #Allow opencv to capture the Depth Stream
        self.depth = cv.VideoCapture(self.kinectDepth_url)

        #Allow opencv to capture the RGB Stream
        self.image = cv.VideoCapture(self.kinectImage_url)

        #Initialising some options with Default values
        self.retrieveFrames = False
        self.tracking = False
        self.nms = True
        self.displayStream = True
        self.showClock = False
        self.showFPS = False
        self.info = False
        
        #Initialize the HOG descriptor/person detector
        self.hog = cv.HOGDescriptor()
        self.hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
    
    @threaded
    def trackPeople(self):

        command = "SEND"
        self.retrieveFrames = True
        self.fpsProcessing = 0

        self.tracking = True

        while self.tracking:
            
            #Start Timing
            start = time.time()

            imageFrame, depthFrame = self.getFrames()

            #Detect People
            frame, boundingBoxes, personCentres = self.detectPeople(imageFrame)
            
            #Add the Goal Position
            frame, goalPosition = self.addGoal(frame)

            if len(boundingBoxes) > 0:
                
                #Add Crosshair Markers
                frame = self.addMarker(frame,personCentres)

                #In an image with multiple people select a person to follow
                personPosition = self.selectPerson(boundingBoxes, personCentres)

                #Determine Image Size
                width = frame.shape[1] 
                height = frame.shape[0]

                speed = self.calcSpeed(personPosition,depthFrame)
                angle = self.calcAngle(goalPosition,personPosition,height,width)

                self.wheelchair.transmitCommand(speed,angle,command)
            
            else:
                self.wheelchair.transmitCommand(0,0,"RUN")
    
            if self.showClock == True:
                frame = self.addClock(frame)

            if self.showFPS == True:
                frame = self.addFPS(frame,self.fpsProcessing)

            if self.displayStream == True:
                #Show the frame
                cv.imshow('Stream of {}'.format(self.kinectImage_url),frame)         
        
            # quit program when 'esc' key is pressed
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.retrieveFrames = False
        self.tracking = False
        cv.destroyAllWindows()

    def getFrames(self):

        ret, depthFrame  = self.depth.read()
        ret, imageFrame  = self.image.read()

        #Flip the frames
        #depthFrame = cv.flip(depthFrame,0)
        #imageFrame = cv.flip(imageFrame,0)

        imageFrame = imutils.resize(imageFrame, width=self.frameWidth)
        depthFrame = imutils.resize(depthFrame, width=self.frameWidth)

        if ret == True:
            return imageFrame, depthFrame
            
    @staticmethod
    def addClock(frame):

        #Add clock to the frame
        font = cv.FONT_HERSHEY_SIMPLEX
        currentDateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
        cv.putText(frame,currentDateTime,(16,20), font, 0.6,(0,0,255),1,cv.LINE_AA)

        return frame
    
    @staticmethod
    def addFPS(frame,fps):

        #Add clock to the frame
        font = cv.FONT_HERSHEY_SIMPLEX
        text = '%.2ffps'%round(fps,2)
        cv.putText(frame,text,(16,44), font, 0.6,(0,0,255),1,cv.LINE_AA)

        return frame

    def detectPeople(self,image):
        
        #Detect people in the passed image
        (boundingBoxes, weights) = self.hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=0.6)
        boxes = len(boundingBoxes)

        if self.nms == True: 
            image, boundingBoxes = self.applyNMS(image,boundingBoxes)
            boxesNMA = len(boundingBoxes)

        else:
            #Draw boxes without NMS
            for (x, y, w, h) in boundingBoxes:
                cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        if self.info == True:
            if self.nms == True:
                #Show additional info
                print("INFO: {}: {} original boxes, {} after suppression".format(self.kinectImage_name, boxes, boxesNMA))
            else:
                #Show additional info
                print("INFO: {}: {} bounding boxes".format(self.kinectImage_name,boxes))
        
        if  len(boundingBoxes) > 0:
            for (xA, yA, xB, yB) in boundingBoxes:
            
                x = int(((xB -xA)/2) + xA)
                y = int(((yB -yA)/2) + yA)
                personCentres = (x,y)
        else:
             personCentres = 0

        return image, boundingBoxes, personCentres
    
    @staticmethod
    def applyNMS(image,boundingBoxes):
        
        #Applying NMS
        boundingBoxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boundingBoxes])
        NMAboundingBoxes = non_max_suppression(boundingBoxes, probs=None, overlapThresh=0.90)
        
        #Draw bounding boxes with NMS
        for (xA, yA, xB, yB) in NMAboundingBoxes:
            cv.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

        return image, NMAboundingBoxes

    @staticmethod
    def addMarker(image,points):
        
        crosshairHeight = 20
        crosshairWidth = 20

        width = image.shape[1] 
        height = image.shape[0]

        for (x, y) in points:
            #Horizontal Line & Vertical Line on Video Image
            cv.line(image,((width-crosshairWidth),height),((width+crosshairWidth),height),(0,0,255),2)
            cv.line(image,(width,(height-crosshairHeight)),(width,(height+crosshairHeight)),(0,0,255),2) 

        return image

    @staticmethod
    def addGoal(image):
        
        offset = 10
        crosshairHeight = 20
        crosshairWidth = 20

        width = image.shape[1] 
        height = image.shape[0]

        goalWidth = int((width/2) - offset)
        goalHeight = int((height/2) - offset)
        
        goalPosition = [goalHeight, goalWidth]

        #Horizontal Line & Vertical Line on Video Image
        cv.line(image,((width-crosshairWidth),height),((width+crosshairWidth),height),(0,0,255),2)
        cv.line(image,(width,(height-crosshairHeight)),(width,(height+crosshairHeight)),(0,0,255),2)

        return image, goalPosition

    #Determine Angle
    def calcAngle(self,goalPositon,personPosition,height,width):
        
        xG = goalPositon[0]
        xP = personPosition[0]

        mappingRange = int(width/2) 

        if xP > xG:
            angle = self.minAngle * (mappingRange/(mappingRange-xP))

        elif xP < xG:
            angle = self.maxAngle * (mappingRange/(xP))

        else:
            angle = 0

        angle = int(angle)
        return angle
     
    #Determine Speed
    def calcSpeed(self,personPosition,depthFrame):

        personDistance = self.calcPersonDistance(personPosition,depthFrame)

        if personDistance < 0.2:
            speed = 0
        elif personDistance >=0.2:
            speed = int(31*personDistance + 20)
        
        if speed > self.maxSpeed:
            speed = self.maxSpeed

        return speed
     
    #Providing the Location of a person, returns their distance away
    def calcPersonDistance(self,personPosition,depthFrame):

        x = personPosition[0]
        y = personPosition[1]

        depthValue = depthFrame[x,y]
        distance = self.distanceCalc(depthValue)

        return distance

    #Returns infomraiton about how far away a point is in and image
    @staticmethod
    def distanceCalc(depth):

        a = -0.0000000069
        b = 0.0000064344
        c = -0.0019066199
        d = 0.2331614352
        e = -9.5744837865
    
        #Second Order Custom Estimation
        distance = (a*math.pow(depth,4))+(b*math.pow(depth,3))+(c*math.pow(depth,2))+(d*depth)+e
    
        return distance
    
    #In image with multiple people, select a target
    @staticmethod
    def selectPerson(boundingBoxes,personCentres):

        box = 0
        largestArea = 0
        
        #Draw bounding boxes with NMS
        for (xA, yA, xB, yB) in boundingBoxes:
            
            boxArea = (xB-xA)*(yB*yA)

            if boxArea > largestArea:
                person = box
                largestArea = boxArea

            box = box + 1

        personPosition = personCentres[person]

        return personPosition

   