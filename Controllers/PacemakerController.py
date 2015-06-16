from Controller import Controller
import Events

class PacemakerController(Controller):
	def __init__(self, mediator):
		super(PacemakerController, self).__init__(mediator)
		self.IsRunning = True
		
	def Notify(self, event):
		if isinstance(event, Events.QuitEvent):
			self.IsRunning = False
		
	def Run(self):
		self.IsRunning = True
		while self.IsRunning:
			self.Mediator.Post(Events.TickEvent())
