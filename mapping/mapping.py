#NAME:  mapping.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for load and generating maps
#COPY:  Copyright 2019, All Rights Reserved, Ryan McCartney

import numpy as np
import cv2 as cv
import csv

class Mapping:

    def __init__(self,unitSize,mapLength,mapWidth):

        #Map Refresh Rate
        self.refreshRate = 100 #Hz

        #Determine matrix for map's size
        self.mapLengthUnits = int(mapLength/unitSize)
        self.mapWidthUnits = int(mapWidth/unitSize)
        self.unitSize = unitSize   

        #Create Blank Map
        self.globalMap = self.generateEmptyMap()
    
    #Generate Random Map Data
    def randomMap(self):
        
        length = self.globalMap.shape[0]
        width = self.globalMap.shape[1]
        size = (length,width)

        #Generate Random Obstacles
        ObstaclesRed = np.random.randint(2,size=size,dtype=np.uint8)*255
        ObstaclesGreen = np.full(size,0,dtype=np.uint8)
        ObstaclesBlue = np.full(size,0,dtype=np.uint8)

        #Generate Random Free Space
        FreeSpaceRed = FreeSpaceGreen = FreeSpaceBlue = np.random.randint(2,size=size,dtype=np.uint8)*255

        #Create Single Set of Channels
        red = ObstaclesRed + FreeSpaceRed
        green = ObstaclesGreen + FreeSpaceGreen
        blue = ObstaclesBlue +FreeSpaceBlue

        #Create a single image with the channels
        self.globalMap = np.dstack((blue, green, red))     
    
    #Resize Map for Screen
    def getViewableMap(self):

        screenHeight = 800
        factor = screenHeight/self.mapLengthUnits

        width = int(self.mapWidthUnits*factor)
        height = int(self.mapLengthUnits*factor)
        mapImage = cv.resize(self.globalMap,(width,height))

        return mapImage

    def generateEmptyMap(self):

        size = (self.mapLengthUnits,self.mapWidthUnits)

        red = np.full(size,0,dtype=np.uint8)
        green = np.full(size,0,dtype=np.uint8)
        blue = np.full(size,0,dtype=np.uint8)

        #Create a single image with the channels
        map = np.dstack((blue, green, red))

        return map
   
    def saveMap(self,path):

        mapFile = open(path,"w+")
        dataEntry = "X,Y,Red,Green,Blue\n"
        mapFile.write(dataEntry)
        
        #Write data into CSV file
        for x in range (0,self.mapLengthUnits):

            for y in range (0,self.mapWidthUnits):

                    if self.globalMap[x,y].all != 0:
      
                        #create a data entry
                        pixelColour = self.globalMap[x,y]
                        dataEntry = str(x) + "," + str(y) + "," + str(pixelColour[2]) + "," + str(pixelColour[1]) + "," + str(pixelColour[0]) + "\n"
                        mapFile.write(dataEntry)
        
        mapFile.close()

    def loadMap(self,path):
        
        self.globalMap = self.generateEmptyMap()

        #Open Map File and Process
        with open(path) as mapFile:
            mapData = csv.reader(mapFile, delimiter=',')
            line = 0

            for row in mapData:
                if line == 0:
                    print(f'INFO: Map data is read as follows: {", ".join(row)}')
                    line += 1
                else:
                    self.globalMap[int(row[0]),int(row[1])] = [int(row[4]),int(row[3]),int(row[2])]
                    line += 1
        
        print('INFO: '+str(line)+" entries added to the map.")
        mapFile.close()
   