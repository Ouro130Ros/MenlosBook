from Entity import Entity

class StaticEntity(Entity):
    def __init__(self, layer, tile_set, tile_id, parameters):
        super(StaticEntity, self).__init__(layer, tile_set, tile_id)
        self.IsPassable = parameters.get("Passable", "T") == "T"
