import random
import copy
import Common

class BasicGenerator:
	def __init__(self, config):
		self.Config = config
		self.XSize = config["XSize"]
		self.YSize = config["YSize"]
		self.ZSize = config["ZSize"]
		self.RoomBuffer = 3

		self.Wall = -1
		self.Ground = -1
		self.Player = -1
		for entity in config["Entities"]:
			if entity["Name"] == "Ground": self.Ground = config["Entities"].index(entity)
			if entity["Name"] == "Wall": self.Wall = config["Entities"].index(entity)
			if entity["Name"] == "Player": self.Player = config["Entities"].index(entity)
		self.RoomDensity = config["RoomDensity"]
		self.MinRoomWidth = config["MinRoomWidth"]
		self.MaxRoomWidth = config["MaxRoomWidth"]
		self.MinRoomHeight = config["MinRoomHeight"]
		self.MaxRoomHeight = config["MaxRoomHeight"]

	def Generate(self):
		self.Map = Common.GenerationMap(self.XSize, self.YSize, self.ZSize)
		self._PopulateRooms()
		self._FillMaze()
		self._ConnectRegions()
		self._TrimEnds()
		self._BuildWalls()
		self._PlacePlayer()
		return self.Map.Map

	def _PlacePlayer(self):
		NotPlaced = True
		while NotPlaced:
			x = random.randint(1, self.XSize-1)
			y = random.randint(1, self.YSize-1)
			if self.Map.GetValue(x,y,0) == self.Ground:
				NotPlaced = False
				self.Map.SetValue(x,y,1,self.Player)

	def _BuildWalls(self):
		for x in range(0, self.XSize):
			for y in range(0, self.YSize):
				if self.Map.GetValue(x,y,0) == -1 and self.Map.GetOrdinalValues(x,y,0).get(self.Ground,0) > 0:
					self.Map.SetValue(x,y,0,self.Wall)

	def _TrimEnds(self):
		Trimmed = True
		while Trimmed:
			Trimmed = False
			for x in range(0, self.XSize):
				for y in range(0, self.YSize):
					if self.Map.GetValue(x,y,0) == self.Ground:
						if self.Map.GetCardinalValues(x,y,0).get(self.Ground, 0) == 1:
							self.Map.SetValue(x,y,0,-1)
							Trimmed = True

	def _FillMaze(self):
		for x in range(0, self.XSize):
			for y in range(0, self.YSize):
				Adjacent = self.Map.GetOrdinalValues(x,y,0)
				if Adjacent.get(self.Ground, 0) > 0 and self.Map.GetValue(x,y,0) == -1:
					self.Map.SetValue(x, y, 1, 1)
		MazeRegions = []
		for x in range(0, self.XSize):
			for y in range(0, self.YSize):
				if self.Map.GetValue(x,y,0) == -1 and self.Map.GetValue(x,y,1) == -1:
					InRegion = False
					for region in MazeRegions:
						if region.Contains((x,y)):
							InRegion = True
					if not InRegion:
						r = self.Map.BuildCardinalRegionOnPoint(x, y, 1, [-1])
						MazeRegions.append(r)
		self.Map.ClearLayer(1)

		for region in MazeRegions:
			RegionPoints = copy.deepcopy(region.Points)
			while len(RegionPoints) > 0:
				EligiblePoints = []
				StartPoint = Common.PopRandom(RegionPoints)

				if self.Map.GetCardinalValues(StartPoint[0], StartPoint[1], 1).get(self.Ground, 0) <= 1:
					if StartPoint[0] > 0 and StartPoint[1] > 0 and StartPoint[0] < self.XSize-1 and StartPoint[1] < self.YSize -1:
						self.Map.SetValue(StartPoint[0], StartPoint[1], 1, self.Ground)
						EligiblePoints += region.GetCardinalPoints(StartPoint)
						while len(EligiblePoints) > 0:
							Candidate = Common.PopRandom(EligiblePoints)
							if self.Map.GetCardinalValues(Candidate[0], Candidate[1], 1).get(self.Ground, 0) == 1:
								if Candidate[0] > 0 and Candidate[1] > 0 and Candidate[0] < self.XSize-1 and Candidate[1] < self.YSize -1:
									self.Map.SetValue(Candidate[0], Candidate[1], 1, self.Ground)
									CardsInRegion = region.GetCardinalPoints(Candidate)
									for cardPoint in CardsInRegion:
										if self.Map.GetValue(cardPoint[0], cardPoint[1], 1) == -1 and self.Map.GetCardinalValues(cardPoint[0], cardPoint[1], 1).get(self.Ground, 0) ==1:
											EligiblePoints.append(cardPoint)
							if Candidate in RegionPoints: RegionPoints.remove(Candidate)

	def _ConnectRegions(self):
		Connectors = []
		for x in range(0, self.XSize):
			for y in range(0, self.YSize):
				if self.Map.GetValue(x,y,0) == -1:
					RoomCard = self.Map.GetCardinalValues(x,y,0)
					MazeCard = self.Map.GetCardinalValues(x,y,1)
					if RoomCard.get(self.Ground, 0) > 0 and MazeCard.get(self.Ground, 0) > 0 and MazeCard.get(1, 0) == 0:
						Connectors.append((x,y))
		
		self.Map.MergeLayers(1,0)
		self.Map.ClearLayer(1)

		Regions = []
		for x in range(0, self.XSize):
			for y in range(0, self.YSize):
				if self.Map.GetValue(x,y,0) == self.Ground and not Common.PointInRegions(Regions, (x,y)):
					Regions.append(self.Map.BuildCardinalRegionOnPoint(x,y,0,[self.Ground]))
		DeleteRegions = []
		for region in Regions:
			if not region.TouchesPoints(Connectors):
				DeleteRegions.append(region)
				for point in region.Points:
					self.Map.SetValue(point[0], point[1], 0, -1)
		
		for toDelete in DeleteRegions:
			Regions.remove(toDelete)

		while len(Connectors) > 0:
			Candidate = Common.PopRandom(Connectors)
			CandCards = self.Map.GetCardinalValues(Candidate[0], Candidate[1], 0)
			self.Map.SetValue(Candidate[0], Candidate[1], 0, self.Ground)
			ConnectedRegions = []
			for region in Regions:
				if region.Touches(Candidate):
					ConnectedRegions.append(region)
			NewRegion = Common.Region()
			for region in ConnectedRegions:
				NewRegion.MergeRegion(region)
				Regions.remove(region)
			Regions.append(NewRegion)
			ConnectorsToRemove = []
			for connector in Connectors:
				RegionCount = 0
				if Common.RegionsTouchingPoint(Regions, connector) < 2:
					ConnectorsToRemove.append(connector)
			for rem in ConnectorsToRemove:
				Connectors.remove(rem)

	def _PopulateRooms(self):
		Failures = 0
		while Failures < self.RoomDensity:
			rW = random.randint(self.MinRoomWidth, self.MaxRoomWidth)
			rH = random.randint(self.MinRoomHeight, self.MaxRoomHeight)
			rX = random.randint(1, self.XSize-rW)
			rY = random.randint(1, self.YSize-rH)

			if not self.Map.DoesRectOverlapExistingValues(rX, rY, rW, rH, 0, self.RoomBuffer, [self.Ground]):
				self.Map.FillRectWithValue(rX, rY, rW, rH, 0, self.Ground)
			else:
				Failures += 1