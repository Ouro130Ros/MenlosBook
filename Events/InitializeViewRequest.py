from Event import Event
class InitializeViewRequest(Event):
    def __init__(self, screenSize):
        self.Name = 'InitializeViewRequest'
        self.ScreenSize = screenSize
