#NAME:  runStream.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python function for running the stream based on a constructed class
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

import threading
from cameraStream import cameraStream
import time

fps = 20

stream = cameraStream(fps)
stream.streamKinectImage()
stream.streamKinectDepth()
stream.streamWebcam()
stream.startServer()

