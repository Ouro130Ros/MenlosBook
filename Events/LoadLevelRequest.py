from Event import Event
class LoadLevelRequest(Event):
	def __init__(self, parameters):
		self.Parameters = parameters