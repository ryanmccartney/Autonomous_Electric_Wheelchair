#NAME: move.py
#DATE: 12/11/2018
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python class for moving the wheelchair in an intuative manner
#COPY: Copyright 2018, All Rights Reserved, Ryan McCartney

import numpy as np
import threading
import time
import math
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
    bootTime = 10

    maxSpeed = 40
    speedLimit = 100

    def __init__(self,host):

        self.host = host
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
        self.reset()

    #Send and Receive Messages with implemented logging
    @threaded
    def gamepad(self):

        pygame.init()
        pygame.joystick.init()

        topSpeed = 30

        gamepads = pygame.joystick.get_count()
        #print("INFO: There are",gamepads,"gamepads connected.")

        j = pygame.joystick.Joystick(0)
        j.init()

        axis = j.get_numaxes()
        #print("INFO: There are",axis,"axis in the gamepad.")

        while 1:

            while self.gamepadRunning:
                
                #Get Current Data
                pygame.event.get()

                xAxisLeft = j.get_axis(0)
                yAxisLeft = j.get_axis(1)
                aButton = j.get_button(0)
                bButton = j.get_button(1)
                yButton = j.get_button(2)
                xButton = j.get_button(3)

                #print("Raw data =",xAxisLeft,",",yAxisLeft)

                #Mapped Data for API 
                speed = int(-yAxisLeft*topSpeed)
                angle = int(-xAxisLeft*100)

                #On button presses start and stop wheelchair
                if aButton == True:
                    self.reset()
                if bButton == True:
                    self.eStop()
                if xButton == True:
                    topSpeed = topSpeed + 1
                    if topSpeed > 100:
                        topSpeed = 100
                    print("INFO: Top Speed is now",topSpeed)
                if yButton == True:
                    topSpeed = topSpeed - 1
                    if topSpeed < 0:
                        topSpeed = 0
                    print("INFO: Top Speed is now",topSpeed)
                
                

                #If new command has been identified then send new data to API
                if (self.setSpeed != speed) or (self.setAngle != angle):
                    self.transmitCommand(speed,angle,"RUN")
                    #print("Mapped speed is",speed,"and the angle is",angle)
                    
    #Converts speed in m/s to arbitay speed for commans
    def convertSeeed(speed):

        #Linear Relationship is used for the conversion
        m = 0.5
        c = -5

        speedArbitary = int(m*speed + c)

        return speedArbitary

    #returns the distance travelled based on the speed 
    def distanceTravelled(speed, time):

        distance = speed*time 
        
        return distance

    #parse response
    def decodeResponse(self, receivedMessage):
        
        if receivedMessage != "":
            data = receivedMessage.split(",")

            if len(data) >= 4:
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
        command = "SEND"
        
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

    #Function to change the turn the wheelchair a specific angle
    def turn(self,angle):

        factor = 40
    
        if angle < 0:
            delay = (-angle)/factor
            self.transmitCommand(50,100,"SEND")
            time.sleep(delay)
            self.transmitCommand(0,0,"SEND")

        elif angle > 0:
            delay = angle/factor
            self.transmitCommand(-50,100,"SEND")
            time.sleep(delay)
            self.transmitCommand(0,0,"SEND")

        else:
            self.transmitCommand(0,0,"SEND")

    #Function to change the move the wheelchair a specific distance in meters
    def move(self,distance):

        factor = 1
        delay = distance/factor

        self.transmitCommand(30,0,"SEND")
        time.sleep(delay)
        self.transmitCommand(0,0,"SEND")  

    #Function to change the move the wheelchair a specific distance in meters
    def changeRadius(self,radius):

        delay = 0.1
        factor = 1
        radius = radius/factor
        radius = int(radius)

        angle = self.setAngle

        while radius > self.setAngle: 
            angle = angle + 1
            self.transmitCommand(self.setSpeed,angle,"SEND")
            time.sleep(delay)
        
        while radius < self.setAngle: 
            angle = angle - 1
            self.transmitCommand(self.setSpeed,angle,"SEND")
            time.sleep(delay)

    #Function to Calculate Speed Lmit bases on the value of the closest point
    def changeAngle(self, angle):

        command = "SEND"
        self.transmitCommand(self.setSpeed,angle,command)
        self.setAngle = angle
        
    def changeSpeed(self, speed):

        speed = int(speed)
        command = "SEND"

        self.transmitCommand(speed,self.setAngle,command)
        self.setSpeed = speed

    #Emergency Stop the wheelchair
    def eStop(self):

        self.transmitCommand(0,0,"STOP")
        print("INFO: Wheelchair has Emergency Stopped.")
    
    #Reset the wheelchair
    def reset(self):

        self.transmitCommand(0,0,"RESET")
        print("INFO: Wheelchair is being reset.")
    
        for x in range(self.bootTime,0,-1):
            print("INFO:",x,"seconds remaining until the wheelchair completes boot up.")
            time.sleep(1)

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

    #Send and Receive Messages with implemented logging
    def transmitCommand(self, speed, angle, command):

        #Start Timing
        start = time.time()

        #Check parameters are ints
        speed = int(speed)
        angle = int(angle)

        #Create form of the payload
        payload = str(speed)+","+str(angle)+","+ command

        #combine with host address
        message = self.host + payload

        response = requests.post(message)
        
        #print(response.url)
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
        #print("STATUS: Sending '",payload,"' took %.2f seconds." % round((end-start),2))