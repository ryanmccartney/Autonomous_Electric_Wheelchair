#NAME:  streamCapture.py
#DATE:  08/02/2019
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

class StreamCapture:

    displayStream = True
    stream = True
    fps = 20
    
    def __init__(self,stream_url,stream_name):
        
        #Get Stream URL
        self.stream_url = stream_url
        self.stream_name = stream_name

        #Allow opencv to capture the stream
        self.image = cv.VideoCapture(self.stream_url)
        self.streamVideo()

    def getFrame(self):

        ret, self.frame = self.image.read()
    
        if ret == True:
            return self.frame
    
    @threaded
    def streamVideo(self):
        
        delay = 1/self.fps

        self.record = False
        self.stream = True
        
        while self.stream == True:
                
            #Get frame from stream
            frame = self.getFrame()
            time.sleep(delay)

            if self.displayStream == True:
                #Show the frame
                cv.imshow('Stream of {}'.format(self.stream_name),frame)                 
            
            # quit program when 'esc' key is pressed
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

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
        out = cv.VideoWriter('data/video/{}_{}.avi'.format(self.stream_name,currentDateTime),fourcc, 20.0, (640,480))

        while(self.image.isOpened()) and (self.record == True):
            ret, frame = self.image.read()
    
            if ret==True:
                #frame = cv.flip(frame,0)

                #write the flipped frame
                out.write(frame)
                time.sleep(delay)

                if self.displayStream == True:
                    cv.imshow('Recording of {}'.format(self.stream_name),frame)

                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        # Release everything if job is finished
        self.record = False
        self.image.release()
        out.release()
        cv.destroyAllWindows()