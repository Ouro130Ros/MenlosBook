class Location:
	def __init__(self, locationXY):
		self.Location = locationXY #(x, y)
		self.Neighbors = [None, None, None, None]
		self.Entities = [] #Entity()
		
	def OnEnter(self, entity):
		pass
	
	def OnExit(self, entity):
		pass

	def OnUpdate(self, CommandEvent):
		pass