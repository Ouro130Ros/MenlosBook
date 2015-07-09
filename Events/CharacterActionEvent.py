from Event import Event

class CharacterActionEvent(Event):
    def __init__(self, inputCommand):
        self.Name = 'CharacterMovementEvent'
        self.Command = inputCommand