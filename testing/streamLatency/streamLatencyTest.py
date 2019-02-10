#NAME: gamepadNavigationAntiCollision.py
#DATE: 08/02/2019
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python function for navigating the wheelchaitr with an XBOX 360 game controller avoiding obstacles
#COPY: Copyright 2019, All Rights Reserved, Ryan McCartney

from streamCapture import StreamCapture
import time


try:
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "INFO = Program has started running." + "\n"
    print(logEntry)

    kinectDepth_url = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
    kinectDepth_name = "Big Buck Bunny Test Stream 1"
    kinectImage_url = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
    kinectImage_name = "Big Buck Bunny Test Stream 2"

    depth = StreamCapture(kinectDepth_url,kinectDepth_name)
    video = StreamCapture(kinectImage_url,kinectImage_name)
    
    #Show Clock
    depth.showClock = True
    video.showClock = True

    #Show Measured FPS
    depth.showFPS = True
    video.showFPS = True

    #Show Stream
    depth.displayStream = True
    video.displayStream = True
   
    while (depth.stream == True) and (video.stream == True):

        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "INFO: Number of Depth Frames Processed ="+ str(depth.framesProcessed)
        print(logEntry)

        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "INFO: Number of Video Frames Processed ="+ str(video.framesProcessed) + "\n"
        print(logEntry)

except:
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "ERROR = Could not process streams." + "\n"
    print(logEntry)
    exit()
