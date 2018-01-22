from math import *
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from startingConfiguration import octohedron, icosahedron

from EnergyCalc.membraneEnergy import energyCalc
energy1 = energyCalc()

# create starting configuration
verts, faces = icosahedron()

# calculate the bending energy of the membrane configuration
Ebend = energy1.calcEbend(verts, faces)

print 'Energy', Ebend
# add MC moves

# for testing

# Print Vertex Positions to File
test = open('testfile.txt','w')  
for i in range(len(faces)):
	print>>test, faces[i]  
test.close() 

#Plot Vertex Positions

x = []
y = []
z = []
for i in range(len(verts)):
	x.append(verts[i][0])
	y.append(verts[i][1])
	z.append(verts[i][2])

fig = plt.figure(1)
ax = Axes3D(fig)
ax.plot(x,y,z,'ro', label='start')
ax.legend(loc='upper left', numpoints = 1)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()
