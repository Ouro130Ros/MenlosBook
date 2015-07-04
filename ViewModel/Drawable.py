import Constants
class Drawable:
    def __init__(self, tile_set, tile_id, layer, location, offset):
        self.WorldLocation = ((location[0]*Constants.TILE_X) - offset[0], (location[1]*Constants.TILE_Y)-offset[1])
        self.TileSet = tile_set
        self.TileID = tile_id
        self.Layer = layer
