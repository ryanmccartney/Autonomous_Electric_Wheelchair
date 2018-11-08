#NAME:  runStream.py
#DATE:  Thursday 8th November 2018
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python function for running the stream based on a constructed class
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

import threading
from cameraStream import cameraStream
import time

try:
    #framerate variable
    fps = 10
    #specifies the starting port for streams
    port = 8080

    #new instance of 'cameraStream' class
    stream = cameraStream(fps,port)

    #Start streams
    stream.streamKinectImage()
    stream.streamKinectDepth()
    #stream.streamWebcam()

except KeyboardInterrupt:

            stream.running = False
            print('INFO: Stopping Program')