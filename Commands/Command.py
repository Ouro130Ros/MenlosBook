class Command(object):
	def __init__(self, entity, actors ,locations):
		self.Entity = entity
		self.Actors = actors
		self.Locations = locations
		self.Alternates = []

	def Execute(self):
		for alternate in self.Alternates:
			ViewUpdate = alternate.Execute()
			if ViewUpdate: return ViewUpdate
		return None

