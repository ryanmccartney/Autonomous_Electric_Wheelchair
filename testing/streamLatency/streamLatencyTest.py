#NAME: gamepadNavigationAntiCollision.py
#DATE: 08/02/2019
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python function for navigating the wheelchaitr with an XBOX 360 game controller avoiding obstacles
#COPY: Copyright 2019, All Rights Reserved, Ryan McCartney

from streamCapture import StreamCapture
import cv2 as cv
import time

fps = 10

try:
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "INFO = Program has started running." + "\n"
    print(logEntry)

    kinectDepth_url = "http://192.168.1.101:8081/?action=stream"
    kinectDepth_name = "Microsoft Kienct V1 Depth Stream"
    kinectImage_url = "http://192.168.1.101:8080/?action=stream"
    kinectImage_name = "Microsoft Kienct V1 RGB Stream"

    depth = StreamCapture(kinectDepth_url,kinectDepth_name)
    video = StreamCapture(kinectImage_url,kinectImage_name)
    
    #Show Clock
    depth.showClock = True
    video.showClock = True

    #Show Measured FPSq
    depth.showFPS = True
    video.showFPS = True

    #Show Stream
    depth.displayStream = True
    video.displayStream = True

    #Record Streams
    #depth.recordVideo()
    #video.recordVideo()
    
    delay = 1/fps
   
    while (depth.stream == True or depth.record == True) and (video.stream == True or video.record == True):

        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "INFO: Number of Depth Frames Processed ="+ str(depth.framesProcessed)
        print(logEntry)

        #Output Test Depth
        cv.imshow('Depth Ouput',depth.frame)

        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "INFO: Number of Video Frames Processed ="+ str(video.framesProcessed) + "\n"
        print(logEntry)

        #Output Test
        cv.imshow('RGB Output',video.frame)

        #Delay
        time.sleep(delay)

        # quit program when 'esc' key is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cv.destroyWindow('Depth Ouput')
    cv.destroyWindow('RGB Output')

except:
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "ERROR = Could not process streams." + "\n"
    print(logEntry)
    exit()
