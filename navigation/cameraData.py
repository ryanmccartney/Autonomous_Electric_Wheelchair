#NAME:  cameraData.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for aquiring image data from network streams
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

import threading
import numpy as np
import cv2 as cv
import time
import imutils

#define threading wrapper
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class cameraData:

    frameWidth = 800
    
    def __init__(self,stream_url,stream_name):
        
        #Get Stream URL
        self.stream_url = stream_url
        self.stream_name = stream_name
        #Allow opencv to capture the stream
        self.image = cv.VideoCapture(self.stream_url)

    def getFrame(self):
        
        #Read a single frame
        self.ret, frame = self.image.read()
        #Resize the frame
        frame = imutils.resize(frame, width=self.frameWidth)

        return frame

    def getFramerate(self):

        frames = 200
        start = time.time()

        for i in range (0,frames):
               
            #Get frame from stream
            frame = self.getFrame()
                     
        #Calculate Frames Per Second
        end = time.time()
        fps = frames/(end-start)  
        fps = round(fps, 3)

        return fps
    
    @threaded
    def streamVideo(self):
        
        font = cv.FONT_HERSHEY_SIMPLEX
        fps = self.getFramerate()

        while(1):
                
            #Get frame from stream
            frame = self.getFrame()

            #Add FPS and  display the frame
            cv.putText(frame,"FPS:{0}".format(fps),(10,500), font, 1,(255,255,255),2,cv.LINE_AA)
            cv.imshow('Stream of {}'.format(self.stream_name),frame)         
        
            # quit program when 'esc' key is pressed
            k = cv.waitKey(5) & 0xFF
            if k == 27:
                break

        cv.destroyAllWindows()
