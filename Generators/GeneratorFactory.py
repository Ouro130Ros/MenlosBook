from BasicGenerator import BasicGenerator

class GeneratorFactory:
    def GetGenerator(self, generatorName, levelConfig):
        if generatorName == "Basic":
            return BasicGenerator(levelConfig)
