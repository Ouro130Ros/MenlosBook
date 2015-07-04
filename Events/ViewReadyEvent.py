from Event import Event

class ViewReadyEvent(Event):
    def __init__(self):
        self.Name = "ViewReadyEvent"