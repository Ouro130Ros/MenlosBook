import Constants
import random

def PopRandom(l):
	return l.pop(random.randrange(0, len(l)))

def RegionsTouchingPoint(regions, p):
	Count = 0
	for region in regions:
		if region.Touches(p): Count += 1
	return Count

def PointInRegions(regions, p):
	for region in regions:
		if region.Contains(p): return True
	return False

class GenerationMap:
	def __init__(self, x, y, z):
		self.XSize = x
		self.YSize = y
		self.ZSize = z
		self.Map = []
		for mX in range(0, x):
			Layer = []
			for mY in range(0, y):
				Column = []
				for mZ in range(0, z):
					Column.append(-1)
				Layer.append(Column)
			self.Map.append(Layer)

	def DoesRectOverlapExistingValues(self, x, y, w, h, z, roomBuffer, valuesRange):
		for rX in range(x-roomBuffer, x+w+roomBuffer):
			for rY in range(y-roomBuffer, y+h+roomBuffer):
				if rX >= self.XSize or rY >= self.YSize or rX < 0 or rY < 0: return True
				if self.Map[rX][rY][z] in valuesRange: return True
		return False

	def FillRectWithValue(self, x, y, w, h, z, value):
		for rX in range(x, x+w):
			for rY in range(y, y+h):
				self.Map[rX][rY][z] = value

	def ClearLayer(self, z):
		for x in range(0, self.XSize):
			for y in range(0, self.YSize):
				self.Map[x][y][z] = -1

	def _AddToCountDict(self, d, val):
		if not val in d.keys(): d[val] = 1
		else: d[val] += 1

	def GetCardinalValues(self, x, y, z):
		Values = {"Locations":[None, None, None, None], "Points":[]}
		if x > 0:
			self._AddToCountDict(Values, self.Map[x-1][y][z])
			Values["Points"].append((x-1,y))
			Values["Locations"][Constants.DIRECTION_W] = self.Map[x-1][y][z]
		if x < self.XSize-1:
			self._AddToCountDict(Values, self.Map[x+1][y][z])
			Values["Points"].append((x+1,y))
			Values["Locations"][Constants.DIRECTION_E] = self.Map[x+1][y][z]
		if y > 0:
			self._AddToCountDict(Values, self.Map[x][y-1][z])
			Values["Points"].append((x,y-1))
			Values["Locations"][Constants.DIRECTION_N] = self.Map[x][y-1][z]
		if y < self.YSize-1:
			self._AddToCountDict(Values, self.Map[x][y+1][z])
			Values["Points"].append((x,y+1))
			Values["Locations"][Constants.DIRECTION_S] = self.Map[x][y+1][z]
		return Values

	def MergeLayers(self, sourceLayer, targetLayer):
		for x in range(0, self.XSize):
			for y in range(0, self.YSize):
				if self.Map[x][y][sourceLayer] >= 0:
					self.Map[x][y][targetLayer] = self.Map[x][y][sourceLayer]

	def SetValue(self, x, y, z, val):
		self.Map[x][y][z] = val

	def GetValue(self, x, y, z):
		return self.Map[x][y][z]

	def GetOrdinalValues(self, x, y, z):
		Values = self.GetCardinalValues(x, y, z)
		Values["Locations"] += [None, None, None, None]
		if x>0 and y>0:
			self._AddToCountDict(Values, self.Map[x-1][y-1][z])
			Values["Points"].append((x-1,y-1))
			Values["Locations"][Constants.DIRECTION_NW] = self.Map[x-1][y-1][z]
		if x>0 and y<self.YSize-1:
			self._AddToCountDict(Values, self.Map[x-1][y+1][z])
			Values["Points"].append((x-1, y+1))
			Values["Locations"][Constants.DIRECTION_SW] = self.Map[x-1][y+1][z]
		if x<self.XSize-1 and y>0:
			self._AddToCountDict(Values, self.Map[x+1][y-1][z])
			Values["Points"].append((x+1,y-1))
			Values["Locations"][Constants.DIRECTION_NE] = self.Map[x+1][y-1][z]
		if x<self.XSize-1 and y<self.YSize-1:
			self._AddToCountDict(Values, self.Map[x+1][y+1][z])
			Values["Points"].append((x+1,y+1))
			Values["Locations"][Constants.DIRECTION_SE] = self.Map[x+1][y+1][z]
		return Values

	def BuildCardinalRegionOnPoint(self, x, y, z, acceptedValues):
		R = Region()
		Queue = []
		Queue.append((x,y))
		while len(Queue) > 0:
			Next = Queue.pop()
			R.Add(Next)
			nX = Next[0]
			nY = Next[1]

			if nX > 0 and self.Map[nX-1][nY][z] in acceptedValues and not R.Contains((nX-1,nY)):
				Queue.append((nX-1,nY))
			if nX < self.XSize - 1 and self.Map[nX+1][nY][z] in acceptedValues and not R.Contains((nX+1, nY)):
				Queue.append((nX+1, nY))
			if nY > 0 and self.Map[nX][nY-1][z] in acceptedValues and not R.Contains((nX, nY-1)):
				Queue.append((nX, nY-1))
			if nY < self.YSize - 1 and self.Map[nX][nY+1][z] in acceptedValues and not R.Contains((nX, nY+1)):
				Queue.append((nX, nY+1))
		return R

	def RegionTouchesCardinalValues(self, region, z, values):
		for point in region.Points:
			CardinalValues = self.GetCardinalValues(point[0], point[1], z) 
			for value in values:
				if CardinalValues.get(value, 0) > 0: return True
		return False

	def Print(self):
		for z in range(0, self.ZSize):
			print '--------------------------'
			for y in range(0, self.YSize):
				line = ''
				for x in range(0, self.XSize):
					line += "{0} ".format('-' if self.Map[x][y][z] == -1 else self.Map[x][y][z])
				print line
	def PrintLayer(self, z):
		print '-------------------'
		for y in range(0, self.YSize):
			line = ''
			for x in range(0, self.XSize):
				line += "{0} ".format('-' if self.Map[x][y][z] == -1 else self.Map[x][y][z])
			print line

class Region:
	def __init__(self):
		self.Points=[]
	
	def Add(self, point):
		self.Points.append(point)

	def GetCardinalPoints(self, point):
		Cardinals = []
		if (point[0]+1, point[1]) in self.Points: Cardinals.append((point[0]+1, point[1]))
		if (point[0]-1, point[1]) in self.Points: Cardinals.append((point[0]-1, point[1]))
		if (point[0], point[1]+1) in self.Points: Cardinals.append((point[0], point[1]+1))
		if (point[0], point[1]-1) in self.Points: Cardinals.append((point[0], point[1]-1))
		return Cardinals

	def Touches(self, point):
		if (point[0]+1, point[1]) in self.Points: return True
		if (point[0]-1, point[1]) in self.Points: return True
		if (point[0], point[1]+1) in self.Points: return True
		if (point[0], point[1]-1) in self.Points: return True
		return False

	def TouchesPoints(self, points):
		for point in points:
			if (point[0]+1, point[1]) in self.Points: return True
			if (point[0]-1, point[1]) in self.Points: return True
			if (point[0], point[1]+1) in self.Points: return True
			if (point[0], point[1]-1) in self.Points: return True
		return False

	def Contains(self, point):
		for p in self.Points:
			if p == point: 
				return True
		return False

	def MergeRegion(self, region):
		self.Points += region.Points

	def TouchesCardinally(self, point):
		for p in self.Points:
			if abs(p[0]-point[0]) <= 1 and abs(p[0]-point[1]) <= 1 and abs(p[0] - x) + abs(p[1]-y) != 2: return True
		return False