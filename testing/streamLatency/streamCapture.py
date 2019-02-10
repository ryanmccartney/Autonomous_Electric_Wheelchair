#NAME:  streamCapture.py
#DATE:  08/02/2019
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for aquiring image data from network streams
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

import threading
import numpy as np
import cv2 as cv
import time
from datetime import datetime
import imutils

#define threading wrapper
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class StreamCapture:

    displayStream = True
    stream = True
    showClock = False
    showFPS = False
    frameWidth = 640
    fps = 30
    framesProcessed = 0
    
    def __init__(self,stream_url,stream_name):
        
        #Get Stream URL
        self.stream_url = stream_url
        self.stream_name = stream_name

        #Allow opencv to capture the stream
        self.image = cv.VideoCapture(self.stream_url)
        self.streamVideo()

        self.fpsActual = self.fps

    def getFrame(self,frameWidth):

        ret, frame = self.image.read()
        self.frame = imutils.resize(frame, width=frameWidth)
    
        if ret == True:
            self.framesProcessed = self.framesProcessed + 1
            return self.frame

    @staticmethod
    def addClock(frame):

        #Add clock to the frame
        font = cv.FONT_HERSHEY_SIMPLEX
        currentDateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
        cv.putText(frame,currentDateTime,(16,20), font, 0.6,(0,0,255),1,cv.LINE_AA)

        return frame
    
    @staticmethod
    def addFPS(frame,fps):

        #Add clock to the frame
        font = cv.FONT_HERSHEY_SIMPLEX
        text = '%.2ffps'%round(fps,2)
        cv.putText(frame,text,(16,44), font, 0.6,(0,0,255),1,cv.LINE_AA)

        return frame
    
    @threaded
    def streamVideo(self):
        
        delay = 1/self.fps

        self.record = False
        self.stream = True
        
        while self.stream == True:

            start = time.time()
                
            #Get frame from stream
            frame = self.getFrame(self.frameWidth)
            time.sleep(delay)

            if self.showClock == True:
                frame = self.addClock(frame)

            if self.showFPS == True:
                frame = self.addFPS(frame,self.fpsActual)

            if self.displayStream == True:
                #Show the frame
                cv.imshow('Stream of {}'.format(self.stream_name),frame)                 
            
            # quit program when 'esc' key is pressed
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            
            end = time.time()
            adjustedDelay = delay-(end-start)

            if adjustedDelay < 0:
                adjustedDelay = 0
                self.fpsActual = 1/(end-start)
            else:
                self.fpsActual = self.fps

            time.sleep(adjustedDelay)

        self.stream = False
        cv.destroyAllWindows()

    @threaded
    def recordVideo(self):
        
        delay = 1/self.fps

        #Get Date and Time
        currentDateTime = time.strftime("%d.%m.%Y-%H.%M.%S")
        self.stream = False
        self.record = True

        # Define the codec and create VideoWriter object
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        out = cv.VideoWriter('testing/streamLatency/{}_{}.avi'.format(self.stream_name,currentDateTime),fourcc, 20.0, (640,480))

        while(self.image.isOpened()) and (self.record == True):
            
            start = time.time()
            frame = self.getFrame(self.frameWidth)
    
            #Flip the frame
            #frame = cv.flip(frame,0)

            #write the  frame
            out.write(frame)
            time.sleep(delay)

            if self.showClock == True:
                frame = self.addClock(frame)
            
            if self.showFPS == True:
                frame = self.addFPS(frame,self.fpsActual)

            if self.displayStream == True:
                cv.imshow('Recording of {}'.format(self.stream_name),frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
           
            end = time.time()
            adjustedDelay = delay-(end-start)

            if adjustedDelay < 0:
                adjustedDelay = 0
                self.fpsActual = 1/(end-start)
            else:
                self.fpsActual = self.fps


            time.sleep(adjustedDelay)

        # Release everything if job is finished
        self.record = False
        self.image.release()
        out.release()
        cv.destroyAllWindows()