from Event import Event

class QuitEvent(Event):
	def __init__(self):
		self.Name = 'QuitEvent'