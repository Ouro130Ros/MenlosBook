from uuid import uuid1

class Entity(object):
    def __init__(self, layer, tileSet, tileID):
        self.Layer = layer
        self.TileSet = tileSet
        self.TileID = tileID
        self.ID = str(uuid1())
        self.IsPassable = True

    def GetLocation(self, locations):
        for row in locations:
            for location in row:
                if self in location.Entities: return location
        return None

    def GetActor(self, actors, actorID):
        for actor in actors:
            if actor.ID == actorID: return actor
        return None

    def OnEnter(self, entity):
        pass

    def OnExit(self, entity):
        pass
