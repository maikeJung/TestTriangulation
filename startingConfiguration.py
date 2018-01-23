# shapes for starting configurations

# TODO fix subdivide

from math import *

def octohedron():
	"""Construct an eight-sided polyhedron"""
	f = sqrt(2.0) / 2.0
	verts = [ \
		[ 0, -1,  0],
		[-f,  0,  f],
		[ f,  0,  f],
		[ f,  0, -f],
		[-f,  0, -f],
		[ 0,  1,  0] ]
	faces = [ \
		(0, 2, 1),
		(0, 3, 2),
		(0, 4, 3),
		(0, 1, 4),
		(5, 1, 2),
		(5, 2, 3),
		(5, 3, 4),
		(5, 4, 1) ]
	return verts, faces

def icosahedron():
	"""Construct an icosahedron (20 faces)"""
	t = ( 1.0 + sqrt(5.0) ) / 2.0
	verts = [ \
		[ -1, t,  0],
		[ 1,  t,  0],
		[ -1,  -t,  0],
		[1,  -t,  0],
		[0,  -1, t],
		[ 0,  1,  t],
		[0, -1, -t],
		[0, 1, -t],
		[t, 0, -1],
		[t, 0, 1],
		[-t, 0, -1],
		[-t, 0, 1] ]
	faces = [ \
		(0, 11, 5),
		(0, 5, 1),
		(0, 1, 7),
		(0, 7, 10),
		(0, 10, 11),
		(1, 5, 9),
		(5, 11, 4),
		(11, 10, 2),
		(10, 7, 6),
		(7, 1, 8),
		(3, 9, 4),
		(3, 4, 2),
		(3, 2, 6),
		(3, 6, 8),
		(3, 8, 9),
		(4, 9, 5),
		(2, 4, 11),
		(6, 2, 10),
		(8, 6, 7),
		(9, 8, 1) ]
	return verts, faces

def subdivide(verts, faces):
	"""Subdivide each triangle into four triangles, pushing verts to the unit sphere"""
	""" not working properly due to the different names for the same vertex """
	triangles = len(faces)
	for faceIndex in range(triangles):

		# Create three new verts at the midpoints of each edge:
		face = faces[faceIndex]
		a, b, c = (verts[vertIndex] for vertIndex in face)
		
		normd = 1.0/sqrt( (a[0] + b[0])*(a[0] + b[0]) + (a[1] + b[1])*(a[1] + b[1]) + (a[2] + b[2])*(a[2] + b[2]) )
		#normd = 0.5
		d = ( normd*(a[0]+b[0]), normd*(a[1] + b[1]), normd*(a[2] + b[2]))
	
		norme = 1.0/sqrt( (b[0] + c[0])*(c[0] + b[0]) + (c[1] + b[1])*(c[1] + b[1]) + (c[2] + b[2])*(c[2] + b[2]) )
		#norme = 0.5
		e = ( norme*(c[0]+b[0]), norme*(c[1] + b[1]), norme*(c[2] + b[2]))

		normf = 1.0/sqrt( (a[0] + c[0])*(a[0] + c[0]) + (c[1] + a[1])*(c[1] + a[1]) + (c[2] + a[2])*(c[2] + a[2]) )
		#normf = 0.5
		f = ( norme*(c[0]+a[0]), norme*(c[1] + a[1]), norme*(c[2] + a[2]))

		verts.append(d)
		verts.append(e)
		verts.append(f)

		# Split the current triangle into four smaller triangles:
		i = len(verts) - 3
		j, k = i+1, i+2
		faces.append((i, j, k))
		faces.append((face[0], i, k))
		faces.append((i, face[1], j))
		faces[faceIndex] = (k, j, face[2])

	return verts, faces

# perform creation
def startingConfig():
	num_subdivisions = 0
	verts, faces = octohedron()
	for x in range(num_subdivisions):
		verts, faces = subdivide(verts, faces)
	return verts, faces

