#NAME:  main.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for aquiring image data from network streams
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

from cameraData import cameraData
from move import move
import json

import threading
from queue import Queue
import time

test_url = "rtsp://admin:BirdCamera@192.168.1.114:554/11"

#Load user adjustable variables from json file
settingsFile = open('navigation\settings.json').read()
settings = json.loads(settingsFile)

# Class instances for various streams
test = cameraData(test_url)
# webcam = cameraData(settings['host']['webcam_url'])
# kinectImage = cameraData(settings['host']['kinectImage_url'])
# kinectDepth = cameraData(settings['host']['kinectDepth_url'])

cameraData.streamVideo(test)
