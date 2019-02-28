#NAME: gamepad.py
#DATE: 27/02/2019
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python function for navigating the wheelchair with an XBOX 360 game controller avoiding obstacles
#COPY: Copyright 2019, All Rights Reserved, Ryan McCartney

import time
import pygame
import serial
import threading

#define threading wrapper
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

@threaded
def runGamepad():

    topSpeed = 40
    
    try:

        #Open Serial Port
        wheelchair = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
    
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "INFO = Gamepad has opened a connection with wheelchair cotroller at "+wheelchair.name+"\n"
        print(logEntry)

        pygame.init()
        pygame.joystick.init()

        #Check number of gamepads
        gamepads = pygame.joystick.get_count()

        #Log Entry
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = str(currentDateTime) + ": " + "INFO = ",str(gamepads)," gamepads avalible." + "\n"
        print(logEntry) 

        if gamepads > 0:

            #Initialise first gamepad
            j = pygame.joystick.Joystick(0)
            j.init()
            
            #Check axis avalible
            axis = j.get_numaxes()
            
            #Log Entry
            currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
            logEntry = str(currentDateTime) + ": " + "INFO = Gamepad with ",str(axis)," axis has been initiated." + "\n"
            print(logEntry) 

            #Initialsie Speed and Angle
            setSpeed = 0
            setAngle = 0
            payload = str(setSpeed) + "," + str(setAngle) + ",RUN" + "\r\n"
            wheelchair.write(payload)

            while 1:
                
                time.sleep(0.2)

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
                    wheelchair.write("0,0,RESET\r\n".encode())
                    print("RESET Command Sent")
                if bButton == True:
                    wheelchair.write("0,0,STOP\r\n".encode())
                    print("STOP Command Sent")
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
                if (setSpeed != speed) or (setAngle != angle):
                    
                    payload = str(speed) + "," + str(angle) + ",RUN" + "\r\n"
                    wheelchair.write(payload.encode())

                    setSpeed = speed
                    setAngle = angle
                    print("Mapped speed is",speed,"and the angle is",angle)

                while wheelchair.in_waiting:
                    info = wheelchair.readline()
                    print(info)
    except:
        #Log Entry
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + "STATUS = No Gamepads are avalible. Have you connected any?" + "\n"
        print(logEntry)