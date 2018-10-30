#NAME:  cameraStream.py
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

    def __init__(self, fps):

        self.fps = fps
        self.running = True
        freenect.sync_stop()

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
        array = array.astype(np.uint8)
        return array

    @threaded
    def startServer(self):

        try:
            self.serverCommand = self.serverCommand + " -o 'output_http.so -w ./www/html'"

            #Run commands to start server
            os.system ("sudo mount -t tmpfs tmpfs /var/www/html/stream/image")
            os.system ("sudo mount -t tmpfs tmpfs /var/www/html/stream/depthImage")
            os.system(self.serverCommand)

        except self.running==False:

            print('INFO: Shutting down the video stream')    
            freenect.sync_stop()
            sys.exit()

    #Method for adding wbecam to the stream
    def streamWebcam(self):

        self.serverCommand = self.serverCommand + " -i input_uvc.so"

    #Threaded method for adding kinect data to the stream
    @threaded
    def streamKinectDepth(self):

        delay = 1/self.fps
        self.serverCommand = self.serverCommand + ' -i "input_file.so -f /var/www/html/stream/depthImage -n depthImage.jpg -d 0"'

        while self.running:

            #get a frame from depth sensor
            depth = self.get_depth()
            #write depth image to file
            cv.imwrite('/var/www/html/stream/depthImage/depthImage.jpg',depth)

            #frame delay
            time.sleep(delay)

        print('INFO: Shutting down Kinect Depth Image Stream')    
        freenect.sync_stop()

    @threaded
    def streamKinectImage(self):

        delay = 1/self.fps
        self.serverCommand = self.serverCommand + ' -i "input_file.so -f /var/www/html/stream/image -n image.jpg -d 0"'

        while self.running:

            #get a frame from depth sensor
            image = self.get_video()
            #write depth image to file
            cv.imwrite('/var/www/html/stream/image/image.jpg',image)

            #frame delay
            time.sleep(delay)
           
        print('INFO: Shutting down Kinect RGB Image Stream')    
        freenect.sync_stop()