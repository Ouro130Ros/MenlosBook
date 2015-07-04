from Actor import Actor
import Commands
import random

class Rat(Actor):
    def __init__(self, layer, tile_set, tile_id, parameters):
        super(Rat, self).__init__(layer, tile_set, tile_id, parameters)
        
    def GetNextAction(self, actors, locations):
        return Commands.MovementCommand(self, actors, locations, random.randint(0, 3))
