from Event import Event

class KeypressEvent(Event):
    def __init__(self, isDown, key):
        self.Name = 'KeypressEvent'
        self.KeyPressed = key
        self.IsKeyDown = isDown