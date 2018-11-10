from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
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

def cuboid_data(o, size=(unitSize,unitSize,unitSize)):
    X = [[[0, unitSize, 0], [0, 0, 0], [unitSize, 0, 0], [unitSize, unitSize, 0]],
         [[0, 0, 0], [0, 0, unitSize], [unitSize, 0, unitSize], [unitSize, 0, 0]],
         [[unitSize, 0, unitSize], [unitSize, 0, 0], [unitSize, unitSize, 0], [unitSize, unitSize, unitSize]],
         [[0, 0, unitSize], [0, 0, 0], [0, unitSize, 0], [0, unitSize, unitSize]],
         [[0, unitSize, 0], [0, unitSize, unitSize], [unitSize, unitSize, unitSize], [unitSize, unitSize, 0]],
         [[0, unitSize, unitSize], [0, 0, unitSize], [unitSize, 0, unitSize], [unitSize, unitSize, unitSize]]]
    X = np.array(X).astype(float)
    for i in range(3):
        X[:,:,i] *= size[i]
    X += np.array(o)
    return X

def plotCubeAt(positions,sizes=None,colors=None, **kwargs):
    if not isinstance(colors,(list,np.ndarray)): colors=["C0"]*len(positions)
    if not isinstance(sizes,(list,np.ndarray)): sizes=[(1,1,1)]*len(positions)
    g = []
    for p,s,c in zip(positions,sizes,colors):
        g.append( cuboid_data(p, size=s) )
    return Poly3DCollection(np.concatenate(g),  
                            facecolors=np.repeat(colors,6, axis=0), **kwargs)

N1 = 10
N2 = 10
N3 = 10

ma = np.random.choice([0,1], size=(N1,N2,N3), p=[0.99, 0.01])
x,y,z = np.indices((N1,N2,N3))-.5
positions = np.c_[x[ma==1],y[ma==1],z[ma==1]]
colors= np.random.rand(len(positions),3)

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect('equal')

pc = plotCubeAt(positions, colors=colors,edgecolor="k")
ax.add_collection3d(pc)

ax.set_xlim([0,1000])
ax.set_ylim([0,1000])
ax.set_zlim([0,1000])
#plotMatrix(ax, ma)
#ax.voxels(ma, edgecolor="k")

plt.show()