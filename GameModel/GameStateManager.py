import Constants
from EntityFactory import EntityFactory
from Actor import Actor
from Player import Player
from Location import Location
import ViewModel

class GameStateManager:
	def __init__(self):
		self._Locations = []
		self._Actors = []
		self.Player = None
		self.CurrentLevel = 0
		self.CurrentLevelConfig = None

	def LoadLevel(self, levelConfig):
		Factory = EntityFactory()
		self.CurrentLevelConfig = levelConfig
		XSize = levelConfig.MapSize[0]
		YSize = levelConfig.MapSize[1]
		ZSize = levelConfig.MapHeight 
		for x in range (0, XSize):
			LocationRow = []
			for y in range(0, YSize):
				LocationRow.append(Location((x,y)))
			self._Locations.append(LocationRow)
		print "Building Locations"
		for x in range (0, XSize):
			for y in range(0, YSize):
				if x > 0: self._Locations[x][y].Neighbors[Constants.DIRECTION_W] = self._Locations[x-1][y]
				if x < (XSize - 1): self._Locations[x][y].Neighbors[Constants.DIRECTION_E] = self._Locations[x+1][y]
				if y > 0: self._Locations[x][y].Neighbors[Constants.DIRECTION_N] = self._Locations[x][y-1]
				if y < (YSize - 1): self._Locations[x][y].Neighbors[Constants.DIRECTION_S] = self._Locations[x][y+1]
		for x in range (0, XSize):
			for y in range(0, YSize):
				for z in range(0, ZSize):
					if levelConfig.IsEntityAt(x,y,z):
						CurrentEntity = Factory.GetEntity(levelConfig.GetEntityAt(x,y,z),z)
						self._Locations[x][y].Entities.append(CurrentEntity)
						if isinstance(CurrentEntity, Actor): self._Actors.append(CurrentEntity)
						if isinstance(CurrentEntity, Player): self.Player = CurrentEntity
					
	def GetViewStateLevelParams(self):
		Parameters = ViewModel.InitializationParameters(self.CurrentLevelConfig.MapSize, [10,10])
		for x in range(0, len(self._Locations)):
			for y in range(0, len(self._Locations[x])):
				for entity in self._Locations[x][y].Entities:
					if not entity.TileSet in Parameters.RequiredTilesets: Parameters.RequiredTilesets.append(entity.TileSet)
					Parameters.AddEntity(ViewModel.ViewEntity(entity.ID, (x,y), entity.Layer, entity.TileSet, entity.TileID))
		return Parameters

	def ApplyCharacterInput(self, inputCommand):
		self.Player.InputCommand = inputCommand

	def OnTick(self):
		Actions = []
		for actor in self._Actors:
			NextAction = actor.GetNextAction(self._Actors, self._Locations)
			if NextAction: Actions.append(NextAction)

		ViewModels = []
		while len(Actions) > 0:
			NextAction = Actions.pop(0)
			Response = NextAction.Execute()
			if Response:
				ViewModels += Response.ViewUpdates
				Actions += Response.Commands
		return ViewModels