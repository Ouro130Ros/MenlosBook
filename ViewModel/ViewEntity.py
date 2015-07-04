import Constants
from copy import copy
from Drawable import Drawable

class ViewEntity:
    def __init__(self, model_id, location, layer, tile_set, tile_id):
        self.Update = True
        self.ModelEntityID = model_id,
        self.Location = (location[0], location[1])
        self.TileSet = tile_set
        self.TileID = tile_id
        self.Layer = layer
        self.Offset = [0,0]
        self.Speed = 0
        self.IsBackward = True
        self.EntitiesUnder = []

    def overlaps_entity(self, entity):
        worldLocation = (self.Location[0] * Constants.TILE_X, self.Location[1]*Constants.TILE_Y)
        entityLocation = entity.get_drawable().WorldLocation
        if worldLocation == entityLocation: return True
        if worldLocation[0]+Constants.TILE_X < entityLocation[0]: return False
        if entityLocation[0]+Constants.TILE_X < worldLocation[0]: return False
        if worldLocation[1]+Constants.TILE_Y < entityLocation[1]: return False
        if entityLocation[1]+Constants.TILE_Y < worldLocation[1]: return False
        return True

    def _offset_overlap(self, last_offset):
        if last_offset[0] > 0 and self.Offset[0] < 0: return True
        if last_offset[0] < 0 and self.Offset[0] > 0: return True
        if last_offset[1] > 0 and self.Offset[1] < 0: return True
        if last_offset[1] < 0 and self.Offset[1] > 0: return True
        return False

    def get_drawable(self):
        lastOffset = copy(self.Offset)
        if self.Offset[0] != 0: 
            if self.IsBackward: self.Offset[0] += self.Speed
            else: self.Offset[0] -= self.Speed
        if self.Offset[1] != 0:
            if self.IsBackward: self.Offset[1] -= self.Speed
            else: self.Offset[1] += self.Speed
        if self._offset_overlap(lastOffset) or self.Offset == [0,0]:
            self.Offset = [0,0]
            self.Update = False

        return Drawable(self.TileSet, self.TileID, self.Layer, self.Location, self.Offset)
