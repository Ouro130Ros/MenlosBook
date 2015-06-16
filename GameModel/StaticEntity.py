from Entity import Entity

class StaticEntity(Entity):
	def __init__(self, layer, tileSet, tileID, parameters):
		super(StaticEntity, self).__init__(layer, tileSet, tileID)
		self.IsPassable = parameters.get("Passable", "T") == "T"