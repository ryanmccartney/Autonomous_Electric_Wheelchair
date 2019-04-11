#NAME: move.py
#DATE: 12/11/2018
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python class for moving the wheelchair in an intuative manner
#COPY: Copyright 2018, All Rights Reserved, Ryan McCartney

import numpy as np
import threading
import time
import urllib
import requests

#define threading wrapper
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper
    
class Control:

    #Received Variables
    batteryVoltage = 0
    rightMotorCurrent = 0
    leftMotorCurrent = 0
    status = "NULL"

    #Intrinsic Parameters
    setSpeed = 0
    setAngle = 0
    command = "SEND"

    maxSpeed = 0
    speedLimit = 100

    def __init__(self,host):

        self.host = host
    
        #Create a file for both transmission and receive logs depending on time
        currentDateTime = time.strftime("%d%m%Y-%H%M%S")
        filename = "data\control\Transmitted Data -" + currentDateTime + ".csv"
        self.transmitLog = open(filename,"w+")
        self.transmitLog.write("Date and Time,Speed,Angle,Command Message\n")
      
        #Initialise Receive Log
        filename = "data\control\Received Data -" + currentDateTime + ".csv"
        self.receiveLog = open(filename,"w+")
        self.receiveLog.write("Date & Time,Battery Voltage(V),Right Current (A),Left Current (A),Status Message\n")

        #Send Message and Retrieve Response
        self.transmitCommand(0,0,"RESET")

    #Send and Receive Messages with implemented logging
    def transmitCommand(self, speed, angle, command):

        #Create form of the payload
        payload = str(speed)+","+str(angle)+","+command
        
        #combine with host address
        message = self.host + payload

        #Send Message and Retrieve Response
        receivedMessage = requests.get(message)

        #Get Date and Time for Log
        currentDateTime = time.strftime("%d%m%Y-%H%M%S")

        #Write log entry regarding data transmitted
        dataEntry = currentDateTime + "," + speed + "," + angle + "," + command + "\n"
        self.transmitLog.write(dataEntry)
     
        #Write log entry regarding response
        dataEntry = currentDateTime + "," + receivedMessage + "\n"
        self.receiveLog.write(dataEntry)

        self.decodeResponse(receivedMessage)

        self.setSpeed = speed
        self.setAngle = angle

    #parse response
    def decodeResponse(self, receivedMessage):
        
        data = receivedMessage.split(",")

        self.batteryVoltage = data[0]
        self.rightMotorCurrent = data[1]
        self.leftMotorCurrent = data[2]
        self.status = data[3]

    #Determine Power Consumption
    def powerConsumed(self):

        self.transmitCommand(self.setSpeed,self.setAngle,"SEND")

        #Accounting for Baseload Current Consumption (A)
        current = 1.25

        #Calculation Carried out using simple P=VI Equation
        current =  current + self.rightMotorCurrent + self.leftMotorCurrent

        power = self.batteryVoltage*current

        return power

    #Speed Ramping Function   
    def rampSpeed(self,speed,acceleration):
         
        delay = 1/acceleration
        
        #Direction Forward
        if speed > 0:
            
            #Accelerate
            if speed > self.setSpeed:

                while speed != self.setSpeed:
            
                    speed = self.setSpeed + 1
                    time.sleep(delay)
                    self.transmitCommand(speed,self.setAngle,self.command)

            #Decelerate
            elif speed < self.setSpeed:

                while speed != self.setSpeed:
            
                    speed = self.setSpeed - 1
                    time.sleep(delay)
                    self.transmitCommand(speed,self.setAngle,self.command)

        #Direcion Reverse
        if speed < 0:
            
            #Accelerate
            if speed < self.setSpeed:

                while speed != self.setSpeed:
            
                    speed = self.setSpeed - 1
                    time.sleep(delay)
                    self.transmitCommand(speed,self.setAngle,self.command)

            #Decelerate
            elif speed > self.setSpeed:

                while speed != self.setSpeed:
            
                    speed = self.setSpeed + 1
                    time.sleep(delay)
                    self.transmitCommand(speed,self.setAngle,self.command)

        return speed


    #Function to Calculate Speed Lmit bases on the value of the closest point
    def calcMaxSpeed(self,closestPoint):
        
        self.maxSpeed = int((closestPoint/255)*100)

        #Prevent Speed higher than the limit set
        if self.maxSpeed > self.speedLimit:

            self.maxSpeed = self.speedLimit

    #Collision Avoidance Algorithm
    @threaded
    def collisionAvoidance(self):

        while 1:

            #If Wheelchair is breaking the Speed Limit (Set by Closest Object)
            if self.setSpeed > self.maxSpeed:
                
                #Determine Rate of Decelleration depending on delta
                decceleration = self.setSpeed - self.maxSpeed

                #Adjust Speed                
                self.rampSpeed(self.maxSpeed,decceleration)

            elif self.setSpeed < self.maxSpeed:

                #Determine Rate of Acceleration depending on delta
                acceleration = self.maxSpeed - self.setSpeed 

                #Adjust Speed                
                self.rampSpeed(self.maxSpeed,decceleration)

    #Converts speed in m/s to arbitary units for commands
    def  getSpeedValue(self,speed):
        #Linear Relationship parmamters for conversion
        m = 0.0319
        c = -0.1

        speedArbitary = int((speed - c)/m)
        return speedArbitary
    
    #Converts speed in arbitary unit to metrics
    def  getSpeedMetric(self,speed):
        #Linear Relationship parmamters for conversion
        m = 0.0319
        c = -0.1

        speedMetric = (m*speed)+c
        speedMetric = round(speedMetric,2)
        return speedMetric



            
            



        