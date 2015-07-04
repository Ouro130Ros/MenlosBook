import Constants
from EntityFactory import EntityFactory
from Actor import Actor
from Player import Player
from Location import Location
import ViewModel

class LevelManager:
    def __init__(self):
        self._Locations = []
        self._Actors = []
        self.Player = None
        self.CurrentLevel = 0
        self.CurrentLevelConfig = None

    def load_level(self, level_config):
        factory = EntityFactory()
        self.CurrentLevelConfig = level_config
        xSize = level_config.MapSize[0]
        ySize = level_config.MapSize[1]
        zSize = level_config.MapHeight
        
        for x in range (0, xSize):
            location_row = list()
            for y in range(0, ySize):
                location_row.append(Location((x, y)))
            self._Locations.append(location_row)

        for x in range (0, xSize):
            for y in range(0, ySize):
                if x > 0: self._Locations[x][y].Neighbors[Constants.DIRECTION_W] = self._Locations[x-1][y]
                if x < (xSize - 1): self._Locations[x][y].Neighbors[Constants.DIRECTION_E] = self._Locations[x+1][y]
                if y > 0: self._Locations[x][y].Neighbors[Constants.DIRECTION_N] = self._Locations[x][y-1]
                if y < (ySize - 1): self._Locations[x][y].Neighbors[Constants.DIRECTION_S] = self._Locations[x][y+1]

        for x in range (0, xSize):
            for y in range(0, ySize):
                for z in range(0, zSize):
                    if level_config.IsEntityAt(x,y,z):
                        currentEntity = factory.GetEntity(level_config.GetEntityAt(x, y, z), z)
                        if z == 1: print currentEntity
                        self._Locations[x][y].Entities.append(currentEntity)
                        if isinstance(currentEntity, Actor): self._Actors.append(currentEntity)
                        if isinstance(currentEntity, Player): self.Player = currentEntity
        print len(self._Actors)
                    
    def GetViewStateLevelParam(self):
        parameters = ViewModel.InitializationParameters(self.CurrentLevelConfig.MapSize, self.Player.GetLocation(self._Locations).Location)
        for x in range(0, len(self._Locations)):
            for y in range(0, len(self._Locations[x])):
                for entity in self._Locations[x][y].Entities:
                    if not entity.TileSet in parameters.RequiredTilesets: parameters.RequiredTilesets.append(entity.TileSet)
                    parameters.add_entity(ViewModel.ViewEntity(entity.ID, (x,y), entity.Layer, entity.TileSet, entity.TileID))
        return parameters

    def ApplyCharacterInput(self, inputCommand):
        self.Player.InputCommand = inputCommand

    def OnTick(self):
        Actions = []
        ViewModels = []
        for actor in self._Actors:
            actor.AddEnergy(1)

        if not (self.Player.CanMove() and self.Player.InputCommand == None):
            for actor in self._Actors:
                if actor.CanMove():
                    NextAction = actor.GetNextAction(self._Actors, self._Locations)
                    if NextAction: Actions.append(NextAction)

            while len(Actions) > 0:
                NextAction = Actions.pop(0)
                Response = NextAction.Execute()
                if Response:
                    ViewModels += Response.ViewUpdates
                    Actions += Response.Commands
        return ViewModels