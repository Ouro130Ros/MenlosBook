from Controller import Controller
from Events import *
from Models import ConfigurationWrapper
import os
import json

class ConfigurationController(Controller):
    def __init__(self, mediator):
        super(ConfigurationController, self).__init__(mediator)
        self.MonitorConfig = False
        self.ConfigTickCount = 0
        self.CurrentTickCount = 0
        self.Configuration = None

    def Notify(self, event):
        if isinstance(event, TickEvent):
            if self.MonitorConfig: print 'TODO: MONITOR CONFIG'
        if isinstance(event, LoadConfigRequestEvent):
            with open(os.getcwd() + '\\Configuration.json') as datafile:
                Config = json.load(datafile)
            self.Configuration = ConfigurationWrapper(Config)
            self.Mediator.Post(LoadConfigResponseEvent(self.Configuration))