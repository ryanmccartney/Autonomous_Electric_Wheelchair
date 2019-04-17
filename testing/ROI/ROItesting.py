#NAME: ROItesting.py
#DATE: 17/04/2019
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python function for identifyinh the ROI of interest in an image
#COPY: Copyright 2019, All Rights Reserved, Ryan McCartney

from datetime import datetime
import numpy as np
import numba as nb
import cv2 as cv
import imutils
import time
import json

#Logging Function (Pretty Console Output)
def log(entry):    

    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + entry

    #open a txt file to use for logging
    logFile = open(logFilePath,"a+")
    logFile.write(logEntry+"\n")
    logFile.close()
    print(logEntry)

def addFPS(frame,fps):
    #Add clock to the frame
    font = cv.FONT_HERSHEY_SIMPLEX
    text = '%.2ffps'%round(fps,2)
    cv.putText(frame,text,(16,44), font, 0.6,(0,0,255),1,cv.LINE_AA)
    return frame

def addClock(frame):
    #Add clock to the frame
    font = cv.FONT_HERSHEY_SIMPLEX
    currentDateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
    cv.putText(frame,currentDateTime,(16,20), font, 0.6,(0,0,255),1,cv.LINE_AA)
    return frame

#Determine Distance Average
def getAverage(frame):
    windowSize = 0.2
    xA = int((frame.shape[1]/2)-(frame.shape[1]*windowSize))
    yA = int((frame.shape[0]/2)-(frame.shape[0]*windowSize))
    xB = int((frame.shape[1]/2)+(frame.shape[1]*windowSize))
    yB = int((frame.shape[0]/2)+(frame.shape[0]*windowSize))
    window =  frame[yA:yB, xA:xB]
    average = np.median(window)
    return average,window

#Use Ceter Average to Determine the Size of the ROI
def determineSize(frame,average):
    normalisedAverage = 1-(average/255)
    heightRatio = frame.shape[1]/frame.shape[0]
    widthRatio = frame.shape[0]/frame.shape[1]
    #ROI Location and Size
    roiWidth = int(frame.shape[1]*(normalisedAverage*widthRatio))
    roiHeight = int(frame.shape[0]*(normalisedAverage*heightRatio))

    if roiWidth < frame.shape[1]*0.3:
        roiWidth = int(frame.shape[1]*0.3)   
    if roiHeight < frame.shape[0]*0.6:
        roiHeight = int(frame.shape[0]*0.6)

    return roiWidth,roiHeight

def getROI(frame,roiWidth,roiHeight):
       
    yA = frame.shape[0]-roiHeight
    yB = frame.shape[0]   
    xA = int((frame.shape[1]-roiWidth)/2)
    xB = int((frame.shape[1]-roiWidth)/2)+roiWidth

    #Crop and Mark
    frameROI =  frame[yA:yB, xA:xB]
    frame = cv.rectangle(frame, (xA,yA), (xB,yB),(0,255,0), 2)
    return frame,frameROI

#Get configuration file details
configurationFile = open('testing/ROI/settings.json').read()
configuration = json.loads(configurationFile)

#Get the details of the log file from the configuration
logFilePath = configuration['general']['logFile']
fps = configuration['general']['fps']
kinectDepth_url = configuration['streams']['kinectDepth']['url']
kinectDepth_name = configuration['streams']['kinectDepth']['name']
kinectImage_url = configuration['streams']['kinectRGB']['url']
kinectImage_name = configuration['streams']['kinectRGB']['name']

#open a txt file to use for logging and clear it
logFile = open(logFilePath,"w")
logFile.close()
log("INFO = ROI test beginning.")

#Allow opencv to capture the stream
image = cv.VideoCapture(kinectImage_url)
depth = cv.VideoCapture(kinectDepth_url)

framesProcessed = 0
frameWidth = 640
fpsAcutal = fps
returned, depthFrame  = depth.read()
returned, imageFrame  = image.read()

while returned == True:

    delay = 1/fps
    start = time.time()

    imageFrame = imutils.resize(imageFrame, width=frameWidth)
    depthFrame = imutils.resize(depthFrame, width=frameWidth)

    #Add FPS and Clock to Image
    imageFrame = addFPS(imageFrame,fpsAcutal)
    imageFrame = addClock(imageFrame)

    #Determine the size of the ROI
    average,window = getAverage(depthFrame)
    roiWidth,roiHeight = determineSize(depthFrame,average)

    #Get ROI
    imageFrame,imageROI = getROI(imageFrame,roiWidth,roiHeight)
    depthFrame,depthROI = getROI(depthFrame,roiWidth,roiHeight)

    #Convert Depth Image to Grayscale
    depthFrame = cv.cvtColor(depthFrame, cv.COLOR_BGR2GRAY)
    depthROI = cv.cvtColor(depthROI, cv.COLOR_BGR2GRAY)

    cv.imshow('Stream of {}'.format(kinectDepth_name),depthFrame)    
    cv.imshow('Stream of {}'.format(kinectImage_name),imageFrame) 

    #Log Data
    framesProcessed = framesProcessed + 1
    log("INFO = Processed frame number "+str(framesProcessed))
    log("INFO = Average center value of depth is "+str(average))

    #Calculate FPS
    end = time.time()
    adjustedDelay = delay-(end-start)

    if adjustedDelay < 0:
        adjustedDelay = 0
        fpsAcutal = 1/(end-start)
    else:
        fpsAcutal = fps

    # quit program when 'esc' key is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        log("INFO = User closed the program.")
        break
            
    time.sleep(adjustedDelay)
    returned, depthFrame  = depth.read()
    returned, imageFrame  = image.read()

log("INFO = Program has been stopped.")
cv.destroyAllWindows()

    
