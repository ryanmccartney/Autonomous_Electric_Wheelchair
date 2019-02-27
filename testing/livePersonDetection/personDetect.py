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
from imutils.object_detection import non_max_suppression
from imutils import paths

#define threading wrapper
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class PersonDetect:

    displayStream = False
    stream = True
    showClock = False
    showFPS = False
    info = False
    frameWidth = 640
    fps = 15
    nms = True
        
    def __init__(self,stream_url,stream_name):
        
        #Get Stream URL
        self.stream_url = stream_url
        self.stream_name = stream_name
        
        #Allow opencv to capture the stream
        self.image = cv.VideoCapture(self.stream_url)
        self.streamVideo()

        #Varible Initialisation for Thread Handling
        self.fpsActual = self.fps
        self.frameID = 0
        self.processedFrameID = self.frameID
        
        #Initialize the HOG descriptor/person detector
        self.hog = cv.HOGDescriptor()
        self.hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
        
    def getFrame(self,frameWidth):

        ret, frame  = self.image.read()

        #Flip the frame
        #nextFrame = cv.flip(nextFrame,0)

        frame = imutils.resize(frame, width=frameWidth)

        self.frameID = self.frameID + 1

        if ret == True:
            return frame,self.frameID

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

    def detectPeople(self,image,frameID):
        
        #Detect people in the passed image
        (rects, weights) = self.hog.detectMultiScale(image, winStride=(4, 4), padding=(16, 16), scale=0.6)
        
        if self.nms == True:
            image, pick = self.applyNMS(image,rects)
        else:
            #Draw boxes without NMS
            for (x, y, w, h) in rects:
                cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        if self.info == True:
            if self.nms == True:
                #Show additional info
                print("INFO: {}: {} original boxes, {} after suppression".format(self.stream_name, len(rects), len(pick)))
            else:
                #Show additional info
                print("INFO: {}: {} bounding boxes".format(self.stream_name, len(rects)))
        
        processedFrame = image
        processedFrameID = frameID

        return processedFrame,processedFrameID
    
    @staticmethod
    def applyNMS(image,rects):
        
        #Applying NMS
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.90)
        
        #Draw bounding boxes with NMS
        for (xA, yA, xB, yB) in pick:
            cv.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
            
        return image, pick

    @threaded
    def streamVideo(self):
        
        delay = 1/self.fps

        self.record = False
        self.stream = True
        
        while self.stream == True:

            start = time.time()

            time.sleep(delay)
            
            streamFrame, frameID = self.getFrame(self.frameWidth)
            processedFrame, self.processedFrameID = self.detectPeople(streamFrame,frameID)
        
            if self.processedFrameID >= frameID:
                
                if self.showClock == True:
                    processedFrame = self.addClock(processedFrame)

                if self.showFPS == True:
                    processedFrame = self.addFPS(processedFrame,self.fpsActual)

                if self.displayStream == True:
                    #Show the frame
                    cv.imshow('Stream of {}'.format(self.stream_name),processedFrame)         
            
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
            recordFrame = self.getFrame(self.frameWidth)
            recordFrame = self.detectPeople(recordFrame)
    
            #write the  frame
            out.write(recordFrame)
            time.sleep(delay)

            if self.showClock == True:
                recordFrame = self.addClock(recordFrame)
            
            if self.showFPS == True:
                recordFrame = self.addFPS(recordFrame,self.fpsActual)

            if self.displayStream == True:
                cv.imshow('Recording of {}'.format(self.stream_name),recordFrame)

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