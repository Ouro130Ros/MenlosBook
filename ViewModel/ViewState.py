from ViewEntity import ViewEntity
from datetime import datetime
import Constants

class ViewState:
	def __init__(self, mapSize, offset, screenSize):
		self.MapSize = mapSize
		self.ScreenSize = screenSize
		self.UpdateAll = False
		self.LastTimestamp = datetime.now()
		self.DrawFrame = True
		self.Entities = []
		self.Offset = offset

	def AddEntity(self, viewEntity):
		self.Entities.append(viewEntity)
		
	def GetDrawableUpdates(self):
		Updates = []
		if self.UpdateAll:
			self.UpdateAll = False
			for e in self.Entities: Updates.append(e.GetDrawable())	
		else:
			for e in self.Entities:
				if e.Update:
					Updates.append(e.GetDrawable())
					for u in e.EntitiesUnder:
						Updates.append(u.GetDrawable())
		return sorted(Updates, key=lambda x: x.Layer)	
			
	def OnTick(self):
		CurrentTime = datetime.now()
		ElapsedTime = (self.LastTimestamp - CurrentTime)
		ElapsedMS = (ElapsedTime.days * 24 * 60 * 60 + ElapsedTime.seconds) * 1000 + ElapsedTime.microseconds / 1000.0
		if ElapsedMS > 42:
			self.DrawFrame = True

	def IsReady(self):
		for e in self.Entities: 
			if e.Update: return False
		return True

	def ShiftOffset(self, delta):
		self.Offset[0] += delta[0]
		self.Offset[1] += delta[1]
		if self.Offset[0] < 0: self.Offset[0] = 0
		if self.Offset[1] < 0: self.Offset[1] = 0
		if self.Offset[0] > (self.MapSize[0]*Constants.TILE_X) - self.ScreenSize[0]:
			self.Offset[0] = (self.MapSize[0]*Constants.TILE_X) - self.ScreenSize[0]
		if self.Offset[1] > (self.MapSize[1]*Constants.TILE_Y) - self.ScreenSize[1]:
			self.Offset[1] = (self.MapSize[1]*Constants.TILE_Y) - self.ScreenSize[1]
	
	def ApplyUpdates(self, updates):
		DeleteEntities = []
		for entity in updates:
			entity.Update = True
			for existingEntity in self.Entities:
				if existingEntity.ModelEntityID == entity.ModelEntityID:
					DeleteEntities.append(existingEntity)
					
		for delete in DeleteEntities:
			if delete in self.Entities:
				self.Entities.remove(delete)

		self.Entities = self.Entities + updates

