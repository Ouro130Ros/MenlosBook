import Constants
from copy import copy
from Drawable import Drawable

class ViewEntity:
    def __init__(self, modelID, location, layer, tileset, tileID):
        self.Update = True
        self.ModelEntityID = modelID,
        self.Location = (location[0], location[1])
        self.TileSet = tileset
        self.TileID = tileID
        self.Layer = layer
        self.Offset = [0,0]
        self.Speed = 0
        self.IsBackward = True
        self.EntitiesUnder = []

    def OverlapsEntity(self, entity):
        WL = (self.Location[0] * Constants.TILE_X, self.Location[1]*Constants.TILE_Y)
        EL = entity.GetDrawable().WorldLocation
        if WL == EL: return True
        return not (WL[0]+Constants.TILE_X<EL[0] or EL[0]+Constants.TILE_X<WL[0] or WL[1]+Constants.TILE_Y<EL[1] or EL[1]+Constants.TILE_Y<WL[1])


    def _OffsetOverlap(self, lastOffset):
        if lastOffset[0] > 0 and self.Offset[0] < 0: return True
        if lastOffset[0] < 0 and self.Offset[0] > 0: return True
        if lastOffset[1] > 0 and self.Offset[1] < 0: return True
        if lastOffset[1] < 0 and self.Offset[1] > 0: return True
        return False

    def GetDrawable(self):
        LastOffset = copy(self.Offset)
        if self.Offset[0] != 0:
            if self.IsBackward: self.Offset[0] += self.Speed
            else: self.Offset[0] -= self.Speed
        if self.Offset[1] != 0:
            if self.IsBackward: self.Offset[1] -= self.Speed
            else: self.Offset[1] += self.Speed
        if self._OffsetOverlap(LastOffset) or self.Offset == [0,0]:
            self.Offset = [0,0]
            self.Update = False

        return Drawable(self.TileSet, self.TileID, self.Layer, self.Location, self.Offset)