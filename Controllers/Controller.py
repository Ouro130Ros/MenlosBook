class Controller(object):
    def __init__(self, mediator):
        self.Mediator = mediator
        self.Mediator.RegisterListener(self)
        
    def Notify(self, event):
        pass
