#NAME:  startup.py
#DATE:  Wednesday 27th November 2018
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python function for running the startup sequence required for the wheelchair controller, streams and data logging
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

import threading
import serial
from cameraStream import cameraStream
import time
import io

#Create a file for logging
try:
    #open a txt file to duse for logging 
    logFile = open("log.txt","w+")
    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "INFO = System is starting up." + "\n"
    logFile.write(logEntry)
    print(logEntry)
except:
    print("ERROR: Unable to open log file.")
    exit()

try:
    #framerate variable
    fps = 10
    #specifies the starting port for streams
    port = 8080

    currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
    logEntry = currentDateTime + ": " + "INFO = Framerate of streams is set as "+str(fps)+"fps and initial stream port is port "+str(port)+"\n"
    logFile.write(logEntry)
    print(logEntry)

    #new instance of 'cameraStream' class
    stream = cameraStream(fps,port)

    #Start streams
    try:
        stream.streamKinectImage()
        time.sleep(2)
        stream.streamKinectDepth()
        time.sleep(2)
        stream.streamWebcam()
        time.sleep(2)   
 
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "INFO = Camera Streams Started."+"\n"
        logFile.write(logEntry)
        print(logEntry)

    except:
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "INFO = Failed to start camera streams."+"\n"
        logFile.write(logEntry)
        print(logEntry)

    try:
        #Open Serial Port
        wheelchair = serial.Serial('/dev/ttyACM0')

        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "INFO = Opened connection with wheelchair cotroller at "+wheelchair.name+"\n"
        logFile.write(logEntry)
        print(logEntry)

    except:
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "ERROR = Failed to open connection with wheelcahir controller. Check serial port."+"\n"
        logFile.write(logEntry)
        print(logEntry)

except KeyboardInterrupt:
            stream.running = False
            print('INFO: Stopping Program')