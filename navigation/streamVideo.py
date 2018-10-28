#!/usr/bin/env python

#NAME:  streamVideo.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for streaming image data as a video using opencv
#NOTE:  Copyright 2018, All Rights Reserved, Ryan McCartney

#-----------------------------------------------------------------------------------------------------------------------
# Imports, Global Variable Definitions & Initialisation
#-----------------------------------------------------------------------------------------------------------------------

from threading import Thread
import numpy as np
import cv2

#-----------------------------------------------------------------------------------------------------------------------
# Class for aquiring camera image data
#-----------------------------------------------------------------------------------------------------------------------
class streamImageData(stream_url):

    def streamVideo:
        
        stream_url = settings['host']['camera_url']

        #Resolution of matrix
        image = cv2.VideoCapture(stream_url)

        while(1):

            #read frram
            ret, frame = image.read()
   
            #display RGB image
            cv2.imshow('RGB image',frame)

        cv2.destroyAllWindows()