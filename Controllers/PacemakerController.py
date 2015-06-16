from Controller import Controller
from Events import TickEvent, QuitEvent

class PacemakerController(Controller):
	def __init__(self, mediator):
		super(PacemakerController, self).__init__(mediator)
		self.IsRunning = True
		
	def Notify(self, event):
		if isinstance(event, QuitEvent):
			self.IsRunning = False
		
	def Run(self):
		self.IsRunning = True
		while self.IsRunning:
			self.Mediator.Post(TickEvent())
