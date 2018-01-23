from math import *
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def surface(slices, stacks, func):
	verts = []
	for i in range(slices + 1):
		theta = i * pi / slices
		for j in range(stacks):
			phi = j * 2.0 * pi / stacks
			p = func(theta, phi)
			verts.append(p)
            
	faces = []
	v = 0
	for i in range(slices):
		for j in range(stacks):
			next = (j + 1) % stacks
			faces.append((v + j, v + next, v + j + stacks))
			faces.append((v + next, v + next + stacks, v + j + stacks))
		v = v + stacks

	return verts, faces

def sphere(u, v):
	x = sin(u) * cos(v)
	y = cos(u)
	z = -sin(u) * sin(v)
	return [x, y, z]

'''
slices, stacks =2,2
verts, faces = surface(slices, stacks, sphere)

print verts, faces
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
'''