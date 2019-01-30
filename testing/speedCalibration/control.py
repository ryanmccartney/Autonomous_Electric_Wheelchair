#NAME: move.py
#DATE: 12/11/2018
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python class for moving the wheelchair in an intuative manner
#COPY: Copyright 2018, All Rights Reserved, Ryan McCartney

import numpy as np
import threading
import time
import requests 
import pygame
from requests import Session

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
    setCommand = "SEND"

    maxSpeed = 0
    speedLimit = 100

    def __init__(self,host):

        self.host = host
        self.sesssion = requests.session()
        self.gamepadRunning = False
        self.gamepad()
    
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
    @threaded
    def gamepad(self):

        pygame.init()
        pygame.joystick.init()

        gamepads = pygame.joystick.get_count()
        print("INFO: There are",gamepads,"gamepads connected.")

        j = pygame.joystick.Joystick(0)
        j.init()

        axis = j.get_numaxes()
        print("INFO: There are",axis,"axis in the gamepad.")

        while 1:

            while self.gamepadRunning:
                
                #Get Current Data
                pygame.event.get()

                xAxisLeft = j.get_axis(0)
                yAxisLeft = j.get_axis(1)

                #print("Raw data =",xAxisLeft,",",yAxisLeft)

                #Mapped Data for API 
                speed = int(-yAxisLeft*100)
                angle = int(-xAxisLeft*100)
               
            
                #If new command has been identified then send new data to API
                if (self.setSpeed != speed) or (self.setAngle != angle):
                    self.transmitCommand(speed,angle,"RUN")
                    print("Mapped speed is",speed,"and the angle is",angle)
                    
    #Send and Receive Messages with implemented logging
    @threaded
    def transmitCommand(self, speed, angle, command):

        #Start Timing
        start = time.time()

        #Create form of the payload
        payload = str(speed)+","+str(angle)+","+ command

        #combine with host address
        message = self.host + payload

        response = self.sesssion.post(message, timeout=2)

        print(response.url)
        #print("INFO: Transmission response code is",str(response.status_code))

        #Get Date and Time for Log
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")

        #Write log entry regarding data transmitted
        dataEntry = currentDateTime + ","+ str(speed) + "," + str(angle) + "," + command + "\n"
        self.transmitLog.write(dataEntry)

        data = response.content.decode("utf-8").split("\r\n")

        if data[0] != "":
            #Write log entry regarding response
            dataEntry = currentDateTime + "," + data[0] + "\n"
            self.receiveLog.write(dataEntry)
            print(dataEntry)
            
            #Decode Data
            self.decodeResponse(data[0])

        if response.status_code == 200:
            self.setSpeed = speed
            self.setAngle = angle
            self.setCommand = command

        end = time.time()
        print("STATUS: Sending '",payload,"'took %.2f seconds." % round((end-start),2))
        thread.exit()

    #Converts speed in m/s to arbitay speed for commans
    def convertSeeed(speed):

        #Linear Relationship is used for the conversion
        m = 0.5
        c = -5

        speedArbitary = int(m*speed + c)

        return speedArbitary

    #returns the distance travelled based on the speed 
    def distanceTravelles(speed, time):

        distance = speed*time 
        
        return distance

    #parse response
    def decodeResponse(self, receivedMessage):
        
        if receivedMessage != "":
            data = receivedMessage.split(",")

            self.batteryVoltage = data[0]
            self.rightMotorCurrent = data[1]
            self.leftMotorCurrent = data[2]
            self.status = data[3]

    #Determine Power Consumption (in Watts)
    def powerConsumed(self):

        self.transmitCommand(self.setSpeed,self.setAngle,"SEND")

        #Accounting for Baseload Current Consumption (A)
        current = 1.25

        #Calculation Carried out using simple P=VI Equation
        current =  current + self.rightMotorCurrent + self.leftMotorCurrent

        power = self.batteryVoltage*current

        return power

    #Speed Ramping Function   
    def rampSpeed(self,newSpeed,acceleration):
         
        delay = 1/acceleration
        delay = int(delay)
        command = "RUN"
        
        #Direction Forward
        if newSpeed >= 0:

            #Accelerate
            if newSpeed > self.setSpeed:
        
                while newSpeed != self.setSpeed:
                    
                    time.sleep(delay)
                    speed = self.setSpeed + 1
                    self.transmitCommand(speed,self.setAngle,command)
                    time.sleep(delay)

            #Decelerate
            elif newSpeed < self.setSpeed:

                while newSpeed != self.setSpeed:
                    
                    time.sleep(delay)
                    speed = self.setSpeed - 1
                    self.transmitCommand(speed,self.setAngle,command)

        #Direcion Reverse
        if newSpeed < 0:
            
            #Accelerate
            if newSpeed < self.setSpeed:

                while newSpeed != self.setSpeed:
            
                    speed = self.setSpeed - 1
                    time.sleep(delay)
                    self.transmitCommand(speed,self.setAngle,command)

            #Decelerate
            elif newSpeed > self.setSpeed:

                while newSpeed != self.setSpeed:
            
                    speed = self.setSpeed + 1
                    time.sleep(delay)
                    self.transmitCommand(speed,self.setAngle,command)

        return newSpeed


    #Function to Calculate Speed Lmit bases on the value of the closest point
    def changeAngle(self, angle):

        command = "SEND"
        self.transmitCommand(self.setSpeed,angle,command)
        self.setAngle = angle
    
    #Emergency Stop the wheelchair
    def eStop(self):

        self.transmitCommand(0,0,"STOP")

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






            
            



        