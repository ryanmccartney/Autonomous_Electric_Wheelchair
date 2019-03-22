#NAME:  lowLatencyTest.py
#DATE:  22/03/2019
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A function for obtaining low latency stream of streamed data
#COPY:  Copyright 2019, All Rights Reserved, Ryan McCartney

import numpy as np
import cv2 as cv
from urllib.request import urlopen
import time

#Retrieve Frame
def getFrame(snapshotURL):

    request = urlopen(snapshotURL)
    array = np.asarray(bytearray(request.read()), dtype="uint8")
    frame = cv.imdecode(array,-1)

    return frame

#Add FPS Value
def addFPS(frame,fps):

    #Add clock to the frame
    font = cv.FONT_HERSHEY_SIMPLEX
    text = '%.2ffps'%round(fps,2)
    cv.putText(frame,text,(16,22), font, 0.6,(0,0,255),1,cv.LINE_AA)

    return frame

fps = 80

depthFrameURL = "http://192.168.1.100:8081/?action=snapshot"
imageFrameURL = "http://192.168.1.100:8080/?action=snapshot"

delay = 1/fps
fpsActual = fps

while 1:

    start = time.time()

    depthFrame = getFrame(depthFrameURL)
    imageFrame = getFrame(imageFrameURL)

    #Apply the FPS Reading
    imageFrame = addFPS(imageFrame,fpsActual)
    depthFrame = addFPS(depthFrame,fpsActual)
    
    #Show the images
    cv.imshow('Depth Data Stream',depthFrame)
    cv.imshow('Image Data Stream',imageFrame)

    end = time.time()
    adjustedDelay = delay-(end-start)

    if adjustedDelay < 0:
        adjustedDelay = 0
        fpsActual = 1/(end-start)
    else:
        fpsActual = fps

    time.sleep(adjustedDelay)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break