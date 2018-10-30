#NAME:  runStream.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python function for running the stream based on a constructed class
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

import threading
from cameraStream import cameraStream
import time

try:
    #framerate variable
    fps = 10

    #new instance of 'cameraStream' class
    stream = cameraStream(fps)

    #Add streams
    #stream.streamWebcam()
    stream.streamKinectImage()
    stream.streamKinectDepth()

    #Start the streams
    stream.startServer()

except KeyboardInterrupt:

            stream.running = False
            print('INFO: Stopping Program')