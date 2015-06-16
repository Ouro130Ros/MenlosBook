from Controller import Controller
from Events import LogEvent

class ConsoleController(Controller):
    def Notify(self, event):
        if isinstance(event, LogEvent):
            print event.Content