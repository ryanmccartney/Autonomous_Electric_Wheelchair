import numpy as np
import datetime
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#SResolution of matrix units in milimeters
unitSize = 100

#Map Length and Width (in milimeters)
length = 100000
width = 100000
#Map Height (in milimeters)
hieght =10000

lengthUnits = length/unitSize
widthUnits = width/unitSize
hieghtUnits = hieght/unitSize

#Cast to integars
lengthUnits = int(lengthUnits)
widthUnits = int(widthUnits)
hieghtUnits = int(hieghtUnits)

print("Length units of map matrix is = ",lengthUnits)
print("Width units of map matrix is = ",widthUnits)
print("Hieght units of map matrix is = ",hieghtUnits)

map = np.zeros((lengthUnits,widthUnits,hieghtUnits))

#Add the ground to the plot
groundDepth = hieghtUnits/3
groundDepth = int(groundDepth)

for i in range (0,groundDepth):

    for j in range (0,widthUnits):

        for k in range (0,lengthUnits):
            
            map[i,j,k] = 1


fig = plt.figure()
ax = fig.axes(projection='3d')

# Data for three-dimensional scattered points
zdata = 15 * np.random.random(100)
xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens')

#Label Map
ax.set_xlabel('Length (mm)')
ax.set_ylabel('Width (mm)')
ax.set_zlabel('Hieght (mm)')

plt.savefig("map.png")
