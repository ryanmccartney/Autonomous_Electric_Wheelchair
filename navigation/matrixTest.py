import numpy as np
import datetime
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json

#Load user adjustable variables from json file
settingsFile = open('navigation\settings.json').read()
settings = json.loads(settingsFile)

#Resolution of matrix
unitSize = settings['map']['unitSize']

#Map Length, Width and Height (in milimeters)
mapLength = settings['map']['length']
mapWidth = settings['map']['width']
mapHieght = settings['map']['hieght']

#Dimenisions of Autonomous Vechile(in milimeters)
vechileLength = settings['vechile']['length']
vechileWidth = settings['vechile']['width']
vechileHieght = settings['vechile']['hieght']

#Determine matrix for map's size
mapLengthUnits = mapLength/unitSize
mapWidthUnits = mapWidth/unitSize
mapHieghtUnits = mapHieght/unitSize

#Cast to integars
mapLengthUnits = int(mapLengthUnits)
mapWidthUnits = int(mapWidthUnits)
mapHieghtUnits = int(mapHieghtUnits)

#Print Status and some information
print("STATUS: Matrix Processing has started")
print("INFO: Length units of map matrix is = ",mapLengthUnits)
print("INFO: Width units of map matrix is = ",mapWidthUnits)
print("INFO: Hieght units of map matrix is = ",mapHieghtUnits)

map = np.zeros((mapLengthUnits,mapWidthUnits,mapHieghtUnits))

#Add the ground to the plot
print("STATUS: Adding Ground to the map")

mapGroundDepth = mapHieghtUnits/4
mapGroundDepth = int(mapGroundDepth)

for i in range (0,mapGroundDepth):

    for j in range (0,mapWidthUnits):

        for k in range (0,mapLengthUnits):
            
            map[k,j,i] = 1

# Data for three-dimensional scattered points
y,x,z = map.nonzero()

print("STATUS: Plotting 3D Graph")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, zdir='z', c= 'blue')
#ax.view_init(60, 35)

#Label Map
ax.set_xlabel('Length Units')
ax.set_ylabel('Width Units')
ax.set_zlabel('Hieght Units')
ax.set_zlim(0,mapHieghtUnits)

plt.savefig('navigation\map.png')

print("STATUS: Program Finished Running")
