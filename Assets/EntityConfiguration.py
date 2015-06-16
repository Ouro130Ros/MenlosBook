class EntityConfiguration:
	def __init__(self, config):
		self.EntityName = config["Name"]
		self.EntityType = config["Type"]
		self.TileID = config["TileID"]
		self.TileSet = config["TileSet"]
		self.Parameters = config.get("Parameters", {})

	def Height(self, z):
		self.Layer = z