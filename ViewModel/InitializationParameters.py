class InitializationParameters:
    def __init__(self, mapSize, center):
        self.RequiredTilesets = []
        self.MapSize = mapSize # (X, Y)
        self.ViewEntities = []
        self.WorldCenter = center

    def AddTileset(self, tileSet):
        if not tileSet in self.RequiredTilesets: self.RequiredTilesets.append(tileSet)

    def AddEntity(self, viewEntity):
        self.ViewEntities.append(viewEntity)