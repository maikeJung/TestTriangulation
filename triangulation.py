from math import *
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random

from startingConfiguration import octohedron, icosahedron
from parametricsurface import surface, sphere

from EnergyCalc.membraneEnergy import energyCalc
energy1 = energyCalc()


def MCmove(verts, faces):
	#perform MC (Monte Carlo) moves to get new configurations
	
	#randomly select vetex:
	#vertex = random.randint(0, len(verts) -1)

	#try to move each vertex once:
	for i in range(len(verts)-1):
		vertex = i

		#Ebend before move:
		xi = verts[vertex][0]
		yi = verts[vertex][1]
		zi = verts[vertex][2]
		Eold = energy1.calcEbend(verts, faces)

		#Displace vertex slightly:
		verts[vertex][0] += random.uniform(-0.01,0.01)
		verts[vertex][1] += random.uniform(-0.01,0.01)
		verts[vertex][2] += random.uniform(-0.01,0.01)
		Enew = energy1.calcEbend(verts, faces)

		#accept or reject move (Metropolis Algorithm)
		kT = 2.0 
		if np.exp(-(Enew-Eold)/kT) < random.uniform(0.0,1.0):
			#undo move
			verts[vertex][0] = xi
			verts[vertex][1] = yi
			verts[vertex][2] = zi

def MCflip(verts, faces):
	#perform MC by flipping vertex
	
	#calculate energy of original system:
	Eold = energy1.calcEbend(verts, faces)

	#randomly select a face:
	face1 = random.randint(0, len(faces) -1)

	edgep1 = faces[face1][0]
	edgep2 = faces[face1][1]
	edgep3 = faces[face1][2]

	#find the adjacent triangl
	found = False
	for a in range(len(faces)):
		if (faces[a][0] == edgep1 or faces[a][1] == edgep1 or faces[a][2] == edgep1) and (faces[a][0] == edgep2 or faces[a][1] == edgep2 or faces[a][2] == edgep2):
			for b in range(3):
				if faces[a][b] != edgep1 and faces[a][b] != edgep2 and faces[a][b] != edgep3:
					face2 = a
					edgep4 = faces[a][b]
					found = True
			if found: break

	if found:
		faces[face1][1] = edgep4

		if faces[face2][0] == edgep1:
			faces[face2][0] = edgep3
		elif faces[face2][1] == edgep1:
			faces[face2][1] = edgep3
		else:
			faces[face2][2] = edgep3

		#calculate energy of the new system:
		Enew = energy1.calcEbend(verts, faces)

		#accept or reject move (Metropolis Algorithm)
		kT = 2.0 
		if np.exp(-(Enew-Eold)/kT) < random.uniform(0.0,1.0):
			#undo move
			faces[face1][1] = edgep2
			if faces[face2][0] == edgep3:
				faces[face2][0] = edgep1
			elif faces[face2][1] == edgep3:
				faces[face2][1] = edgep1
			else:
				faces[face2][2] = edgep1

# create starting configuration
slices, stacks = 6, 6
verts, faces = surface(slices, stacks, sphere)
#verts, faces = icosahedron()

#number of MC steps
steps = 1000

# store starting config
x = []
y = []
z = []
for i in range(len(faces)):
	for j in range(3):
		x.append(verts[ faces[i][j] ][0])
		y.append(verts[ faces[i][j] ][1])
		z.append(verts[ faces[i][j] ][2])

# Print Starting Positions to File
test = open('starting_config_sphere_vertices'+str(slices*stacks)+'_steps'+str(steps)+'.txt','w')  
for i in range(len(verts)):
	print>>test, verts[i][0], verts[i][1], verts[i][2]  
test.close() 


# calculate the bending energy of the membrane configuration
Ebend = energy1.calcEbend(verts, faces)

print 'Energy of starting config:', Ebend


# perform MC moves
for i in range(steps):
	MCmove(verts, faces)
	for j in range(slices*stacks):
		MCflip(verts, faces)
	Enew = energy1.calcEbend(verts, faces)
	print 'step, Enew:', i, Enew


# Print Final Positions to File
test = open('final_config_sphere_vertices'+str(slices*stacks)+'_steps'+str(steps)+'.txt','w')  
for i in range(len(verts)):
	print>>test, verts[i][0], verts[i][1], verts[i][2]  
test.close() 

# for testing
#Plot Vertex Positions

xf = []
yf = []
zf = []
for i in range(len(verts)):
	xf.append(verts[i][0])
	yf.append(verts[i][1])
	zf.append(verts[i][2])

xt = []
yt = []
zt = []
for i in range(len(faces)):
	for j in range(3):
		xt.append(verts[ faces[i][j] ][0])
		yt.append(verts[ faces[i][j] ][1])
		zt.append(verts[ faces[i][j] ][2])

fig = plt.figure(1)
ax = Axes3D(fig)
ax.plot(x,y,z,'r', label='start')
ax.plot(xf,yf,zf,'bo', label='final')
ax.plot(xt,yt,zt,'b', label='final')
ax.legend(loc='upper left', numpoints = 1)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.text2D(0.75, 0.9, 'vertices:' + str(slices*stacks) + '\n' + 'steps:' + str(steps), transform=ax.transAxes)

plt.show()
