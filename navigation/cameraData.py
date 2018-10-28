#NAME:  cameraData.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for aquiring image data from network streams
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

import numpy as np
import cv2 as cv
import time

class cameraData:

    frameWidth = 500

    def __init__(self,stream_url):
        
        self.stream_url = stream_url

    def getFrame(self):
        
        #Resolution of matrix
        image = cv.VideoCapture(self.stream_url)

        #read single frame
        self.ret, frame = image.read()
        #frame = imutils.resize(frame, width=self.frameWidth)

        return frame
    
    def streamVideo(self):
        
        while(1):

            frame = self.getFrame()
            #display the stream
            cv.imshow('Video Live Stream',frame)
            
            # quit program when 'esc' key is pressed
            k = cv.waitKey(5) & 0xFF
            if k == 27:
                break

        cv.destroyAllWindows()
