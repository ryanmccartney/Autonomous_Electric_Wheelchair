#NAME:  main.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for aquiring image data from network streams
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

from cameraData import cameraData
#from move import move
import json

from threading import Thread
from queue import Queue
import time


test_url = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"

#Load user adjustable variables from json file
settingsFile = open('navigation\settings.json').read()
settings = json.loads(settingsFile)

# Class instances for various streams
test = cameraData(test_url,"Big Buck")
test1 = cameraData(test_url,"Big Buck 1")
# webcam = cameraData(settings['host']['webcam_url'],"Webcam")
# kinectImage = cameraData(settings['host']['kinectImage_url'],"Kinect RGB Image")
# kinectDepth = cameraData(settings['host']['kinectDepth_url'],"Kinect Depth Image")

test.streamVideo()
test1.streamVideo()
#webcam.streamVideo()
