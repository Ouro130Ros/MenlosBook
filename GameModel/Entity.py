from uuid import uuid1

class Entity(object):
    def __init__(self, layer, tile_set, tile_id):
        self.Layer = layer
        self.TileSet = tile_set
        self.TileID = tile_id
        self.ID = str(uuid1())
        self.IsPassable = True

    def GetLocation(self, locations): 
        for row in locations:
            for location in row:
                if self in location.Entities: return location
        return None

    def GetActor(self, actors, actor_id):
        for actor in actors:
            if actor.ID == actor_id: return actor
        return None

    def OnEnter(self, entity):
        pass

    def OnExit(self, entity):
        pass
