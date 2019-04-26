#NAME:  mappingSaveTest.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  Generation of a Random Map and Saving to File
#COPY:  Copyright 2019, All Rights Reserved, Ryan McCartney

import cv2 as cv
from mapping import Mapping
import time

#Initialise Mapping
map = Mapping(0.1,20,20) 
print('INFO: Mapping initialised.')

#Generate Random Map
map.randomMap()
print('INFO: Generated random map.')

#Save Map to File
start = time.time()
mapLocation = 'data/maps/mapTest1.csv'
map.saveMap(mapLocation)
end = time.time()

delay = end - start
text = 'INFO: %.2fs taken to save map.'%round(delay,2)
print(text)

while 1:
    cv.imshow('Global Map',map.getViewableMap())         
            
    #Quit program when 'q' key is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()