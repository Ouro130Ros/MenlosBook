from Event import Event

class UpdateViewEvent(Event):
	def __init__(self, updates):
		self.Name = 'UpdateViewEvent'
		self.Updates = updates