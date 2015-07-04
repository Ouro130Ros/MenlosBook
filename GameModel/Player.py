from Actor import Actor
import UserInput
import Commands

class Player(Actor):
    def __init__(self, layer, tile_set, tile_id, parameters):
        super(Player, self).__init__(layer, tile_set, tile_id, parameters)
        self.InputCommand = None

    def GetNextAction(self, actors, locations):
        if self.InputCommand:
            if isinstance(self.InputCommand, UserInput.MovementInput):
                command = Commands.MovementCommand(self, actors, locations, self.InputCommand.Direction)
                self.InputCommand = None
                return command
