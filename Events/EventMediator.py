from weakref import WeakKeyDictionary
from copy import copy
from TickEvent import TickEvent

class EventMediator:
    def __init__(self):
        self.Listeners = WeakKeyDictionary()
        self.EventQueue = []

    def RegisterListener(self, listener):
        self.Listeners[listener] = 1

    def UnregisterListener(self, listener):
        if listener in self.Listeners.keys():
            del self.Listeners[listener]

    def Post(self, event):
        if not isinstance(event, TickEvent):
            self.EventQueue.append(event)
        else:
            Events = copy(self.EventQueue)
            self.EventQueue = []

            while len(Events) > 0:
                ev = Events.pop(0)
                for listener in self.Listeners.keys():
                    listener.Notify(ev)
            for listener in self.Listeners.keys():
                listener.Notify(event)