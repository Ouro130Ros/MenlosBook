import Constants
class Drawable:
	def __init__(self, tileSet, tileID, layer, location, offset):
		self.WorldLocation = ((location[0]*Constants.TILE_X) - offset[0], (location[1]*Constants.TILE_Y)-offset[1])
		self.TileSet = tileSet
		self.TileID = tileID
		self.Layer = layer
