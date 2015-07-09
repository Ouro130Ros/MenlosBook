from Actor import Actor
import Commands
import random

class Rat(Actor):
    def __init__(self, layer, tileSet, tileID, parameters):
        super(Rat, self).__init__(layer, tileSet, tileID, parameters)

    def GetNextAction(self, actors, locations):
        return Commands.MovementCommand(self, actors, locations, random.randint(0,3))