from math import *
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random

from startingConfiguration import octohedron, icosahedron

from EnergyCalc.membraneEnergy import energyCalc
energy1 = energyCalc()


def MCmove(verts, faces):
	#beforme MC moves to get new configurations
	
	#randomly select vetex:
	vertex = random.randint(0, len(verts) -1)
	#Ebend before move:
	xi = verts[vertex][0]
	yi = verts[vertex][1]
	zi = verts[vertex][2]
	Eold = energy1.calcEbend(verts, faces)

	#Displace vertex slightly:
	verts[vertex][0] += random.uniform(-0.1,0.1)
	verts[vertex][1] += random.uniform(-0.1,0.1)
	verts[vertex][2] += random.uniform(-0.1,0.1)
	Enew = energy1.calcEbend(verts, faces)

	#accept or reject move (Metropolis)
	if Enew < Eold:
		print 'accepted'
	elif np.exp(-(Enew-Eold)/1.0) > random.uniform(0.0,1.0):
		print 'acdepted 2'
	else:
		print 'rejected'
		#undo move
		verts[vertex][0] = xi
		verts[vertex][1] = yi
		verts[vertex][2] = zi

# create starting configuration
verts, faces = icosahedron()

# store starting config
x = []
y = []
z = []
for i in range(len(verts)):
	x.append(verts[i][0])
	y.append(verts[i][1])
	z.append(verts[i][2])

# calculate the bending energy of the membrane configuration
Ebend = energy1.calcEbend(verts, faces)

print 'Energy of starting config:', Ebend

# perform MC moves
for i in range(1000):
	MCmove(verts, faces)
	Enew = energy1.calcEbend(verts, faces)
	print 'Enew', Enew

# for testing

# Print Vertex Positions to File
test = open('testfile.txt','w')  
for i in range(len(faces)):
	print>>test, faces[i]  
test.close() 

#Plot Vertex Positions

xf = []
yf = []
zf = []
for i in range(len(verts)):
	xf.append(verts[i][0])
	yf.append(verts[i][1])
	zf.append(verts[i][2])

fig = plt.figure(1)
ax = Axes3D(fig)
ax.plot(x,y,z,'ro', label='start')
ax.plot(xf,yf,zf,'bo', label='final')
ax.legend(loc='upper left', numpoints = 1)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()
