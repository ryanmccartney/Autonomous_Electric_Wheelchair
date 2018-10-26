import numpy as np
import cv2
import json

#Load user adjustable variables from json file
settingsFile = open('navigation/settings.json').read()
settings = json.loads(settingsFile)

#Get Stream URL from .json settings file
stream_url = settings['host']['camera_url']

#Resolution of matrix
image = cv2.VideoCapture(stream_url)

while(1):

    #read frram
    ret, frame = image.read()
   
    #display RGB image
    cv2.imshow('RGB image',frame)

    #Close on ESC
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
            
cv2.destroyAllWindows()