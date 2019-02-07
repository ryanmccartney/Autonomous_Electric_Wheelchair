#NAME:  imageProcessing.py
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

class imageProcessing:

    frameWidth = 500
    
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
        
        while(1):
                
            #Get frame from stream
            frame = self.getFrame()

            #Show the frame
            cv.imshow('Stream of {}'.format(self.stream_name),frame)         
        
            # quit program when 'esc' key is pressed
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        cv.destroyAllWindows()

    @threaded
    def recordVideo(self):
        
        #Get Date and Time
        currentDateTime = time.strftime("%d.%m.%Y-%H.%M.%S")
    
        # Define the codec and create VideoWriter object
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        out = cv.VideoWriter('data/video/{}_{}.avi'.format(self.stream_name,currentDateTime),fourcc, 20.0, (640,480))

        while(self.image.isOpened()):
            ret, frame = self.image.read()
    
            if ret==True:
                #frame = cv.flip(frame,0)

                #write the flipped frame
                out.write(frame)

                cv.imshow('Recording of {}'.format(self.stream_name),frame)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        # Release everything if job is finished
        self.image.release()
        out.release()
        cv.destroyAllWindows()