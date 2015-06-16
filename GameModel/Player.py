from Actor import Actor
import UserInput
import Commands

class Player(Actor):
	def __init__(self, layer, tileSet, tileID, parameters):
		super(Player, self).__init__(layer, tileSet, tileID, parameters)
		self.InputCommand = None

	def GetNextAction(self, actors, locations):
		if self.InputCommand:
			if isinstance(self.InputCommand, UserInput.MovementInput):
				Command = Commands.MovementCommand(self, actors, locations, self.InputCommand.Direction)
				self.InputCommand = None
				return Command
