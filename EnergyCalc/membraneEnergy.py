# calc energy of a certain configuration

import numpy as np


class energyCalc():
	def __init__(self):
		self.kapa = 1.0

	def createFaceList(self, vert, faces):
		# find all faces that contain a certain vertex
		faceList = []
		for faceIndex in range(len(faces)):
			if (faces[faceIndex][0] == int(vert) or faces[faceIndex][1] == int(vert) or faces[faceIndex][2] == int(vert) ):
				faceList.append(faces[faceIndex])
		return faceList

	def createEdgeList(self, vert, faceList):
		# find all edges that belong to a certain vertex (so the other vertex of the edge)
		edgeList = []
		for faceIndex in range(len(faceList)):
			for i in range(3):
				if faceList[faceIndex][i] != vert:
					edgeList.append(faceList[faceIndex][i])
		# eliminate the doulbe edges
		edgeList = list(set(edgeList))
		return edgeList

	def calcPhi(self, vert1, edgeListIndex, faceList, verts1):
		# calculate the angle between the unit normal vectors of two triangles sharing an edge

		# define all vectors
		i = verts1[vert1]
		j = verts1[edgeListIndex]
		ijVec = np.subtract(i,j)

		#find remeining vertices
		mnlist = []
		for a in range(len(faceList)):
			if faceList[a][0] == edgeListIndex or faceList[a][1] == edgeListIndex or faceList[a][2] == edgeListIndex:
				for b in range(3):
					if faceList[a][b] != vert1 and faceList[a][b] != edgeListIndex:
						mnlist.append(faceList[a][b])

		if len(mnlist) < 2:
			phi = np.pi
		else:
			m = verts1[mnlist[0]]
			n = verts1[mnlist[1]]

			# define remaining two vectors
			inVec = np.subtract(i,n)
			imVec = np.subtract(i,m) 

			# calculate normal vectors of the two faces
			n1 = np.cross(imVec, ijVec)
			norm1 = np.linalg.norm(n1)
			if norm1 <= 0.0000001: 
				norm1 = 1.0
			n1 = n1/norm1

			n2 = np.cross(ijVec, inVec)
			norm2 = np.linalg.norm(n2)
			if norm2 <= 0.0000002: 		
				norm2 = 1.0
			n2 = n2/norm2

			# calculate the angle between the two normal vectors
			test = np.dot(n1,n2)
			if test >= 1.0: test = 0.999999999999999999

			phi = np.arccos( test )

		return phi
	
	def calcLength(self, vert, edge, verts):
		# calculate length of an edge
		i = verts[vert]
		j = verts[edge]
		ijVec = np.subtract(i,j)
		length = np.linalg.norm(ijVec)
	
		return length

	def calcM(self, vertex, faces, verts):
		# calculate the mean curvature curvature contribution M of a vertex
		M = 0.0

		faceList = self.createFaceList(vertex, faces)
		edgeList = self.createEdgeList(vertex, faceList)

		for i in range(len(edgeList)):
			#calculate the angle between to faces
			phi = self.calcPhi(vertex, edgeList[0], faceList, verts)

			# calculate length of edge
			length = self.calcLength(vertex, edgeList[0], verts)

			M += phi*length

		M *= 0.25

		return M

	def calcAreaTriangel(self, face, verts):
		# calculate area of a face (triangel) using Herons formula
		A = verts[face[0]]
		B = verts[face[1]]
		C = verts[face[2]]
		a = np.linalg.norm( np.subtract(B,C) )
		b = np.linalg.norm( np.subtract(A,C) )
		c = np.linalg.norm( np.subtract(A,B) )

		s = (a+b+c)*0.5
		area = np.sqrt( s*(s-a)*(s-b)*(s-c) )

		return area

	def calcA(self, vertex, faces, verts):
		# calculate the area corresponding to a vertex
		A = 0.0

		faceList = self.createFaceList(vertex, faces)
		for i in range(len(faceList)):
			A += self.calcAreaTriangel(faceList[i], verts)

		A *= 1.0/3.0
		return A

	def calcEbend(self, verts, faces):
		# calulate the bending energy of the membrane
		Ebend = 0.0

		for i in range(len(verts)):
			M = self.calcM(i, faces, verts)
			A = self.calcA(i, faces, verts)
			Ebend += M*M/A

		Ebend *= 2*self.kapa

		return Ebend