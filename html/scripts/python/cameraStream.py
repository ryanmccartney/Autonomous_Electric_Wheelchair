#NAME:  cameraStream.py
#DATE:  Thursday 8th November 2018
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for creating netowrk streams
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

import threading
import freenect
import time
import os
import sys
import cv2 as cv
import numpy as np

#define threading wrapper
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class cameraStream:
    
    serverCommand = "mjpg_streamer"
    running = False
    depth = False
    image = False

    def __init__(self, fps, port):

        self.fps = fps
        self.port = port
        self.running = True

        #Run command to mount directory in RAM
        os.system ("sudo mount -t tmpfs tmpfs /var/www/html/stream")

        self.getKinectData()

    #function to get RGB image from kinect
    @staticmethod
    def get_video():
        array,_ = freenect.sync_get_video()
        array = cv.cvtColor(array,cv.COLOR_RGB2BGR)
        return array
 
    #function to get depth image from kinect
    @staticmethod
    def get_depth():
        array,_ = freenect.sync_get_depth()
        redChannel = array       
        redChannel = upperArray.astype(np.uint8)
        blueChannel = array
        blueChannel >>= 8
        blueChannel = blueChannel.astype(np.uint8)
        blueChannel <<= 6
        greenChannel = np.zeros(array.shape, dtype=np.uint8) 
        frame = np.dstack((redChannel, greenChannel, blueChannel))
        return frame

    #Method for streaming webcam at a port
    @threaded
    def streamWebcam(self):

        try:
            print "INFO: Adding V4L Webcam to stream on port ",str(self.port),"." 
            startWebcamStream = self.serverCommand + " -o 'output_http.so -w ./www/html -p "+ str(self.port)+"' -i input_uvc.so"
            os.system(startWebcamStream)
            self.port = self.port + 1

        except self.running==False:

            print "INFO: Shutting down the V4l Webcam Stream"    
            sys.exit()     

    #Method for streaming kinect RGB image on a port
    @threaded
    def streamKinectImage(self):
        
        try:
            self.image = True
            self.port = self.port + 1
            port = self.port -1
            print "INFO: Adding kinect RGB image to stream on port ",str(port),"."
            startKinectImageStream = self.serverCommand + " -o 'output_http.so -w ./www/html -p "+ str(port) +"' -i 'input_file.so -f /var/www/html/stream -n image.jpg -d 0'"
            os.system(startKinectImageStream)

        except self.running==False:

            print "INFO: Shutting down the kinect RGB image stream"
            self.image = False
            freenect.sync_stop()    
            sys.exit()   

    #Method for streaming kinect Depth image on a port
    @threaded
    def streamKinectDepth(self):

        try:
            self.depth = True
            self.port = self.port + 1
            port = self.port -1
            print "INFO: Adding kinect depth images to stream on port ",str(port),"." 
            startKinectDepthStream = self.serverCommand + " -o 'output_http.so -w ./www/html -p "+ str(port) +"' -i 'input_file.so -f /var/www/html/stream -n depthImage.jpg -d 0'"
            os.system(startKinectDepthStream)

        except self.running==False:

            print "INFO: Shutting down the kinect depth image stream"
            self.depth = False    
            freenect.sync_stop()
            sys.exit()   

    #Threaded method for adding kinect data to the stream
    @threaded
    def getKinectData(self):

        delay = 1/self.fps

        #Wait to ports are setup before streaming
        time.sleep(10)
        freenect.sync_stop()

        while self.running:
            
            if self.depth == True:

                #get a frame from depth sensor
                depth = self.get_depth()
                #write depth image to file
                cv.imwrite('/var/www/html/stream/depthImage.jpg',depth)

            if self.image == True:

                #get a frame from depth sensor
                image = self.get_video()
                #write depth image to file
                cv.imwrite('/var/www/html/stream/image.jpg',image)

            #frame delay
            time.sleep(delay)

        print "INFO: Shutting down Kinect Data Capture."  
        freenect.sync_stop()
