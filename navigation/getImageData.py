#!/usr/bin/env python

#NAME:  getCameraData.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for aquiring image data from network streams
#NOTE:  Copyright 2018, All Rights Reserved, Ryan McCartney

#-----------------------------------------------------------------------------------------------------------------------
# Imports, Global Variable Definitions & Initialisation
#-----------------------------------------------------------------------------------------------------------------------

from threading import Thread
import numpy as np
import cv2
import json

#-----------------------------------------------------------------------------------------------------------------------
# Class for aquiring camera image data
#-----------------------------------------------------------------------------------------------------------------------
class getImageData:

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        #Load user adjustable variables from json file
        settingsFile = open('navigation/settings.json').read()
        settings = json.loads(settingsFile)

    def getKinectImage(self):
        #Get Stream URL from .json settings file
        stream_url = settings['host']['kinectImage_url']

        #Resolution of matrix
        image = cv2.VideoCapture(stream_url)

        #read single frame
        ret, frame = image.read()

        return frame

    def getKinectDepth(self):
          #Get Stream URL from .json settings file
        stream_url = settings['host']['kinectDepth_url']

        #Resolution of matrix
        image = cv2.VideoCapture(stream_url)

        #read single frame
        ret, frame = image.read()

        return frame

    def getWebcamImage(self):

        #Get Stream URL from .json settings file
        stream_url = settings['host']['webcam_url']

        #Resolution of matrix
        image = cv2.VideoCapture(stream_url)

        #read single frame
        ret, frame = image.read()

        return frame
