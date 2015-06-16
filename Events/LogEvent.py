from Event import Event

class LogEvent(Event):
	def __init__(self, content):
		self.Name = 'LogEvent'
		self.Content = content