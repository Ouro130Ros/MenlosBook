from Command import Command
from CommandResponse import CommandResponse
from ViewModel import ViewEntity
import GameModel
import Constants

class MovementCommand(Command):
    def __init__(self, entity, actors, locations, direction):
        super(MovementCommand, self).__init__(entity, actors, locations)
        self.Direction = direction

    def _CanMove(self, currentLocaton):
        TargetLocation = currentLocaton.Neighbors[self.Direction]
        if TargetLocation:
            if len(TargetLocation.Entities) == 0: return False
            for entity in TargetLocation.Entities:
                if isinstance(entity, GameModel.StaticEntity) and not entity.IsPassable: return False
                if isinstance(entity, GameModel.Actor): return False
                #TODO Add Checks for Static Entity Movement Costs
            return True

    def Execute(self):
        CurrentLocation = self.Entity.GetLocation(self.Locations)

        if self._CanMove(CurrentLocation):
            self.Entity.CurrentEnergy -= 10
            TargetLocation = CurrentLocation.Neighbors[self.Direction]
            CurrentLocation.Entities.remove(self.Entity)
            ExitCommands = CurrentLocation.on_exit(self.Entity)
            TargetLocation.Entities.append(self.Entity)
            EnterCommands = TargetLocation.on_enter(self.Entity)

            Response = CommandResponse()
            CurrentViewEntity = ViewEntity(self.Entity.ID, TargetLocation.Location, self.Entity.Layer, self.Entity.TileSet, self.Entity.TileID)
            CurrentViewEntity.Speed = self.Entity.Speed
            for entity in CurrentLocation.Entities:
                CurrentViewEntity.EntitiesUnder.append(ViewEntity(entity.ID, CurrentLocation.Location, entity.Layer, entity.TileSet, entity.TileID))
            for entity in TargetLocation.Entities:
                if entity.ID != self.Entity.ID:
                    CurrentViewEntity.EntitiesUnder.append(ViewEntity(entity.ID, TargetLocation.Location, entity.Layer, entity.TileSet, entity.TileID))


            if self.Direction == Constants.DIRECTION_N:
                CurrentViewEntity.Offset=[0,-1*Constants.TILE_Y]
                CurrentViewEntity.IsBackward = False
            if self.Direction == Constants.DIRECTION_S:
                CurrentViewEntity.Offset=[0,Constants.TILE_Y]
                CurrentViewEntity.IsBackward = True
            if self.Direction == Constants.DIRECTION_E:
                CurrentViewEntity.Offset=[Constants.TILE_X,0]
                CurrentViewEntity.IsBackward = False
            if self.Direction == Constants.DIRECTION_W:
                CurrentViewEntity.Offset=[-1*Constants.TILE_X,0]
                CurrentViewEntity.IsBackward = True
            Response.ViewUpdates.append(CurrentViewEntity)
            return Response
        return super(MovementCommand, self).Execute()