#NAME: gamepadNavigationAntiCollision.py
#DATE: 08/02/2019
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python function for navigating the wheelchaitr with an XBOX 360 game controller avoiding obstacles
#COPY: Copyright 2019, All Rights Reserved, Ryan McCartney

from personDetect import PersonDetect
import cv2 as cv
import time

try:
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "INFO = Program has started running." + "\n"
    print(logEntry)

    fps = 25

    delay = 1/fps

    stream_url = "http://192.168.1.102:8080/?action=stream"
    stream_name = "Kinect Image URL"
    
    stream = PersonDetect(stream_url,stream_name) 

    #Show Clock
    stream.showClock = True
    
    #Show Measured FPS
    stream.showFPS = True
    
    #Show Stream
    stream.displayStream = True
    
    #Show Extra Info
    stream.info = True

    #NMS on or off
    stream.nms = True
    
    #Record Streams
    #stream.recordVideo()
    
   
    while (stream.stream == True or stream.record == True):

        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "INFO: Number of Video Frames Processed = "+ str(stream.processedFrameID)
        print(logEntry)
    
        #Delay
        time.sleep(delay)

except:
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "ERROR = Could not process streams." + "\n"
    print(logEntry)
    exit()
