class InitializationParameters:
    def __init__(self, map_size, center):
        self.RequiredTilesets = []
        self.MapSize = map_size # (X, Y)
        self.ViewEntities = []
        self.WorldCenter = center

    def add_tileset(self, tile_set):
        if tile_set not in self.RequiredTilesets: self.RequiredTilesets.append(tile_set)

    def add_entity(self, view_entity):
        self.ViewEntities.append(view_entity)
