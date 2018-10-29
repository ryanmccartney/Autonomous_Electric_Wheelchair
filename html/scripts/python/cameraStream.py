#NAME:  cameraStream.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for creating netowrk streams
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

import threading
import freenect
import time
import os
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

    def __init__(self, fps):

        self.fps = fps

    #function to get RGB image from kinect
    def get_video():
        array,_ = freenect.sync_get_video()
        array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
        return array
 
    #function to get depth image from kinect
    def get_depth():
        array,_ = freenect.sync_get_depth()
        array = array.astype(np.uint8)
        return array

    @threaded
    def startServer(self):

        self.serverCommand = self.serverCommand + " -o 'output_http.so -w ./www/html'"

        #Run commands to start server
        os.system ("sudo mount -t tmpfs tmpfs /var/www/html/stream")
        os.system(self.serverCommand)


    def streamWebcam(self):

        self.serverCommand = self.serverCommand + " -i input_uvc.so"

    @threaded
    def streamKinectDepth(self):

        delay = 1/self.fps

        self.serverCommand = self.serverCommand + ' -i "input_file.so -f /home/pi/stream -n depthImage.jpg -r"'

        while 1:

            #get a frame from depth sensor
            depth = get_depth()
            #write depth image to file
            cv.imwrite('/var/www/html/stream/depthImage.jpg',depth)

            #frame delay
            time.sleep(delay)

    @threaded
    def streamKinectImage(self):

        delay = 1/self.fps

        self.serverCommand = self.serverCommand + ' -i "input_file.so -f /home/pi/stream -n iamge.jpg -r"'

        while 1:

            #get a frame from depth sensor
            image = get_video()
            #write depth image to file
            cv.imwrite('/var/www/html/stream/image.jpg',image)

            #frame delay
            time.sleep(delay)