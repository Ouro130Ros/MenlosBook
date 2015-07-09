from EntityConfiguration import EntityConfiguration
import Generators

class LevelConfiguration:
    def __init__(self, config):
        self.MapType = config["MapType"]
        self.MapSize = (config["XSize"], config["YSize"])
        self.MapHeight = config["ZSize"]
        self.RequiredTilesets = config["TileSets"]
        self.Entities = []
        for entity in config["Entities"]:
            self.Entities.append(EntityConfiguration(entity))
        if self.MapType == "Fixed":
            RawMap = config["Map"]
            self.Map = []
            for x in range(0, config["XSize"]):
                layer = []
                for y in range(0, config["YSize"]):
                    row = []
                    for z in range(0, config["ZSize"]):
                        row.append(RawMap[z][y][x])
                    layer.append(row)
                self.Map.append(layer)
        elif self.MapType == "Generated":
            self.Map = Generators.GeneratorFactory().GetGenerator(config["Method"], config).Generate()


    def GetEntityAt(self, x, y, z):
        return self.Entities[self.Map[x][y][z]]

    def IsEntityAt(self, x, y, z):
        return self.Map[x][y][z] >= 0

