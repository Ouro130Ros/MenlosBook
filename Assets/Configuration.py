from LevelConfiguration import LevelConfiguration
import os
import json
CONFIG_GAMESCREEN = 'GameScreen'

class Configuration:
    def __init__(self):
        with open(os.getcwd() + '\\Configuration.json') as datafile:
            self.ConfigDictionary = json.load(datafile)

    def GetWindowSize(self):
        return (self.ConfigDictionary[CONFIG_GAMESCREEN]['X'], self.ConfigDictionary[CONFIG_GAMESCREEN]['Y'])

    def GetLevel(self, levelNum):
        return LevelConfiguration(self.ConfigDictionary["LevelConfigs"][self.ConfigDictionary["LevelProgression"][levelNum]])