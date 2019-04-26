#NAME:  mappingLoadTest.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  Loading Map from CSV file test
#COPY:  Copyright 2019, All Rights Reserved, Ryan McCartney

import cv2 as cv
from mapping import Mapping
import time

#Initialise Mapping
map = Mapping(0.1,40,60) 
print('INFO: Mapping initialised.')

#Load Map from File
start = time.time()
mapLocation = 'data/maps/mapTest1.csv'
map.loadMap(mapLocation)
end = time.time()

delay = end - start
text = 'INFO: %.2fs taken to load map.'%round(delay,2)
print(text)

while 1:
    #Show map in Window
    cv.imshow('Global Map',map.getViewableMap())         
            
    #Quit program when 'q' key is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()