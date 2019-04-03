#NAME: move.py
#DATE: 08/02/2019
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python class for moving the wheelchair in an intuative manner
#COPY: Copyright 2019, All Rights Reserved, Ryan McCartney

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
    bootTime = 8

    debug = False

    def __init__(self,configuration):

        self.connected = False
        self.dataAge = time.time()+60

        #Load Configuration Variables
        try:
            self.host = configuration['control']['url']
            self.maxSpeed = configuration['control']['maxSpeed']
            
            #Get the details of the log file from the configuration
            self.logFilePath = configuration['general']['logFile']
            self.logging = True

            #Open log file
            try:
                self.log("INFO = Control class has accessed log file.")
            except:
                self.logging = False
                self.log("ERROR: Unable to access log file when initialising control interface.")

        except:
            self.log("ERROR = The configuration file cannot be decoded.")
    
        self.gamepadRunning = False
        self.gamepad()
        
        #Open Transmission and Receive Log Files
        try:            
            #Initialise Transmit Log
            self.transmitLogFilePath = configuration['general']['transmitLog']
            transmitLog = open(self.transmitLogFilePath,"w")
            transmitLog.write("Date and Time,Speed,Angle,Command Message\n")
            transmitLog.close()
      
            #Initialise Receive Log
            self.receiveLogFilePath = configuration['general']['receiveLog']
            receiveLog = open(self.receiveLogFilePath,"w")
            receiveLog.write("Date & Time,Battery Voltage(V),Right Current (A),Left Current (A),Status Message\n")
            receiveLog.close()
            
            #Log Entry
            self.log("INFO = Opened Log files for transmission and receive data.")

        except:
            self.log("ERROR = Could not open transmit and receive logs.")

        #Send Message and Retrieve Response
        self.reset()      
        self.log("INFO = Control interface initialised succesfully.")
  
    #Logging Function
    def log(self, entry):
        
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + entry

        if self.logging == True:
            #open a txt file to use for logging
            logFile = open(self.logFilePath,"a+")
            logFile.write(logEntry+"\n")
            logFile.close()

        print(logEntry)
    
    #Receive Log Function
    def receiveLog(self, entry):
        
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + "," + entry

        if self.logging == True:
            #open a txt file to use for logging
            logFile = open(self.receiveLogFilePath,"a+")
            logFile.write(logEntry+"\n")
            logFile.close()

    #Transmit Log Function
    def transmitLog(self, entry):
        
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + entry

        if self.logging == True:
            #open a txt file to use for logging
            logFile = open(self.transmitLogFilePath,"a+")
            logFile.write(logEntry+"\n")
            logFile.close()

    #Send and Receive Messages with implemented logging
    @threaded
    def gamepad(self):
    
        topSpeed = 30

        try:
            pygame.init()
            pygame.joystick.init()

            #Check number of gamepads
            gamepads = pygame.joystick.get_count()

            #Log Entry
            self.log("INFO = "+str(gamepads)+" gamepads avalible.")

            if gamepads > 0:
            
                #Initialise first gamepad
                j = pygame.joystick.Joystick(0)
                j.init()
            
                #Check axis avalible
                axis = j.get_numaxes()
            
                #Log Entry
                self.log("INFO = Gamepad with "+str(axis)+" axis has been initiated.")

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
                            self.log("INFO = Top Speed is now "+str(topSpeed))
                        if yButton == True:
                            topSpeed = topSpeed - 1
                            if topSpeed < 0:
                                topSpeed = 0
                            self.log("INFO = Top Speed is now "+str(topSpeed))
                
                        #If new command has been identified then send new data to API
                        if (self.setSpeed != speed) or (self.setAngle != angle):
                            self.transmitCommand(speed,angle,"SEND")
                            #print("Mapped speed is",speed,"and the angle is",angle)
        except:
            #Log Entry
            self.log("STATUS = No Gamepads are avalible. Have you connected any?")
                         
    #Converts speed in m/s to arbitay speed for commans
    def convertSeeed(self,speed):
        #Linear Relationship is used for the conversion
        m = 0.5
        c = -5

        speedArbitary = int(m*speed + c)
        return speedArbitary

    #returns the distance travelled based on the speed 
    @staticmethod
    def distanceTravelled(speed, time):

        distance = speed*time  
        return distance

    #parse response
    def decodeResponse(self, receivedMessage):
        
        if receivedMessage != "":
            data = receivedMessage.split(",")

            if len(data) >= 4:
                self.batteryVoltage = float(data[2])
                self.rightMotorCurrent = float(data[0])
                self.leftMotorCurrent = float(data[1])
                self.status = data[3]
        
        self.dataAge = time.time()

    #Determine battery percentage
    def batteryPercent(self):
        
        percent = ((self.batteryVoltage - 23.6)/2)*100
        percent = round(percent,2)

        if percent < 0:
            percent = 0
        elif percent > 100:
            percent = 100

        return percent

    #Determine Power Consumption (in Watts)
    def powerConsumed(self):

        #self.transmitCommand(self.setSpeed,self.setAngle,"SEND")

        #Accounting for Baseload Current Consumption (A)
        current = 0.9

        #Calculation Carried out using simple P=VI Equation
        current =  current + self.rightMotorCurrent + self.leftMotorCurrent

        #P=V*I
        power = self.batteryVoltage*current
        
        #Round to 2 Decimal Places
        power = round(power,2)
        return power

    #Speed Ramping Function   
    def rampSpeed(self,newSpeed,acceleration):

        #Update Variables Before Starting
        self.getUpdate()

        delay = 1/acceleration
        delay = int(delay)
        command = "RUN"

        #Direction Forward
        if newSpeed >= 0:

            #Accelerate
            if newSpeed > self.setSpeed:
        
                while (newSpeed != self.setSpeed) and (self.connected == True):
                    
                    speed = self.setSpeed + 1
                    self.transmitCommand(speed,self.setAngle,command)
                    time.sleep(delay)

            #Decelerate
            elif newSpeed < self.setSpeed:

                while (newSpeed != self.setSpeed) and (self.connected == True):
                    
                    speed = self.setSpeed - 1
                    self.transmitCommand(speed,self.setAngle,command)
                    time.sleep(delay)

        #Direcion Reverse
        if newSpeed < 0:
            
            #Accelerate
            if newSpeed < self.setSpeed:

                while (newSpeed != self.setSpeed) and (self.connected == True):
            
                    speed = self.setSpeed - 1
                    time.sleep(delay)
                    self.transmitCommand(speed,self.setAngle,command)

            #Decelerate
            elif newSpeed > self.setSpeed:

                while (newSpeed != self.setSpeed) and (self.connected == True):
            
                    speed = self.setSpeed + 1
                    time.sleep(delay)
                    self.transmitCommand(speed,self.setAngle,command)

        if self.connected == True:
            self.log("INFO = Speed has been ramped to "+str(newSpeed)+" with an acceleration of "+str(acceleration))
        else:
            self.log("ERROR = Wheelchair speed cannot be ramped.")

        return newSpeed
    
    #Function to change the turn the wheelchair a specific angle
    def turn(self,angle):

        factor = 40
    
        if angle < 0:
            delay = (-angle)/factor
            self.transmitCommand(30,100,"SEND")
            time.sleep(delay)
            self.transmitCommand(0,0,"SEND")

        elif angle > 0:
            delay = angle/factor
            self.transmitCommand(-30,100,"SEND")
            time.sleep(delay)
            self.transmitCommand(0,0,"SEND")

        else:
            self.transmitCommand(0,0,"SEND")
        
        if self.connected == True:
            self.log("INFO = Wheelchair has turned "+str(angle)+" degrees.")
        else:
            self.log("ERROR = Wheelchair has not turned as requested.")

    #Function to change the move the wheelchair a specific distance in meters
    def move(self,distance):

        factor = 1
        delay = int(distance/factor)

        self.transmitCommand(30,0,"SEND")
        time.sleep(delay)
        self.transmitCommand(0,0,"SEND")  

        if self.connected == True:
            self.log("INFO = Wheelchair has moved "+str(distance)+"m.")
        else:
            self.log("ERROR = Wheelchair cannot be moved.")

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
        
        if self.connected == True:
            self.log("INFO = Wheelchair turning radius is now "+str(radius)+"m.")
        else:
            self.log("ERROR = Wheelchair turning radius cannot be changed.")

    #Function to Calculate Speed Lmit bases on the value of the closest point
    def changeAngle(self, angle):

        command = "SEND"
        self.transmitCommand(self.setSpeed,angle,command)

        if self.connected == True:
            self.setAngle = angle
            self.log("INFO = Wheelchair turning angle is now "+str(angle))
        else:
            self.log("ERROR = Wheelchair angle cannot be changed")

    def changeSpeed(self, speed):

        speed = int(speed)
        command = "SEND"

        self.transmitCommand(speed,self.setAngle,command)
        
        if self.connected == True:
            self.setSpeed = speed
            self.log("INFO = Wheelchair speed is now set as "+str(speed))
        else:
            self.log("ERROR = Wheelchair speed cannot be changed")

    #Emergency Stop the wheelchair
    def eStop(self):

        self.transmitCommand(0,0,"STOP")

        if self.connected == True:
            self.log("INFO: Wheelchair has Emergency Stopped.")
        else:
            self.log("ERROR = Warning, the Wheelchair cannot be stopped!")
    
    #Reset the wheelchair
    def reset(self):

        self.transmitCommand(0,0,"RESET")

        if self.connected == True:
            self.log("INFO = Wheelchair is being reset.")
       
            for x in range(self.bootTime,0,-1):
                self.log("INFO = "+str(x)+" seconds remaining until wheelchair completes boot up.")
                time.sleep(1)
        else:
            self.log("ERROR = Wheelchair cannot be reset.")

    #Funtion to Update Variables
    def getUpdate(self):
        
        refreshRate = 5
        elapsedTime = time.time() - self.dataAge 

        if elapsedTime > refreshRate:
            self.transmitCommand(self.setSpeed,self.setAngle,"SEND")

            if self.connected == False:
                self.log("INFO = Communication link down.")
    
    #Function to Calculate Speed Lmit bases on the value of the closest point
    def calcMaxSpeed(self,closestObject):
        
        x = closestObject
        a = -5.6593
        b = 29.089
        c = -5.1123
        d = 3.3333

        #Third Order Deceleration Custom Profile
        maxSpeedNew = (a*math.pow(x,3))+(b*math.pow(x,2))+(c*x)+d
        maxSpeedNew = round(maxSpeedNew,2)

        self.maxSpeed = int(maxSpeedNew)

        #Prevent Speeds higher than the limit set
        if self.setSpeed > 0:
            speedMagnitude = int(self.setSpeed)
            if speedMagnitude > self.maxSpeed:
                self.transmitCommand(self.maxSpeed,self.setAngle,"SEND")
       
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
                self.rampSpeed(self.maxSpeed,acceleration)

    #Send and Receive Messages with implemented logging
    def transmitCommand(self, speed, angle, command):

        #Start Timing
        start = time.time()

        #Make sure values passed are integars
        speed = int(speed)
        angle = int(angle)

        #Check speed does not exceed limit
        if speed > 0:
            if speed > self.maxSpeed:
                speed = self.maxSpeed

        #Create form of the payload
        payload = str(speed)+","+str(angle)+","+ command

        #combine with host address
        message = self.host + payload

        try:
            response = requests.post(message,timeout=2)
            data = response.content.decode("utf-8").split("\r\n")

            if self.debug == True:
                self.log("INFO = Transmission response code is "+str(response.status_code))

            #Write log entry regarding data transmitted
            self.transmitLog(str(speed) + "," + str(angle) + "," + command)

            if data[0] != "":
                #Write log entry regarding response
                self.receiveLog(data[0])
                self.log("STATUS = Received data is as follows; " + data[0])
            
                #Decode Data
                self.decodeResponse(data[0])

            if response.status_code == 200:
                self.connected = True
                self.setSpeed = speed
                self.setAngle = angle
                self.setCommand = command
      
            if self.debug == True:
                end = time.time()
                print("STATUS: Sending '",payload,"' took %.2f seconds." % round((end-start),2))

        except:
            self.log("ERROR = Could not access wheelchair API")
            self.connected = False