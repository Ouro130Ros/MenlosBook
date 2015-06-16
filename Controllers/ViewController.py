import pygame
import Events
from Controller import Controller
import Constants
import Assets
import ViewModel

class ViewController(Controller):
	def __init__(self, mediator):
		super(ViewController, self).__init__(mediator)
		self.ViewState = None
		self.TileSets = {}
		self.WorldScreen = None
		pygame.init()
		self.State = Constants.VIEWSTATE_UNINITIALIZED
		self.WorldSize = None
		
	def InitializeWindow(self, size):
		self.Window = pygame.display.set_mode(size)
		self.WorldSize = size
		pygame.display.set_caption("The House on Warsaw Lane")
		self.Window.fill((0, 0, 0))
		pygame.display.update()
		
	def DrawUpdate(self, drawable):
		#print "Drawing " + drawable.TileID +" at: " + str(drawable.WorldLocation) 
		self.TileSets[drawable.TileSet].BlitOnSurface(self.WorldScreen, drawable)

		
	def UpdateDisplay(self):
		if self.ViewState:
			if self.ViewState.DrawFrame:
				Updates = self.ViewState.GetDrawableUpdates()
				for drawable in Updates:
					self.DrawUpdate(drawable)
				self.Window.blit(self.WorldScreen, (0,0), (self.ViewState.Offset[0], self.ViewState.Offset[1], self.ViewState.Offset[0]+self.WorldSize[0], self.ViewState.Offset[1]+self.WorldSize[1]))
				pygame.display.update()
				if self.ViewState.IsReady():
					self.State = Constants.VIEWSTATE_READY
					self.Mediator.Post(Events.ViewReadyEvent())
		
	def Notify(self, event):
		if isinstance(event, Events.TickEvent):
			if self.State != Constants.VIEWSTATE_UNINITIALIZED: self.UpdateDisplay()
					
		if isinstance(event, Events.InitializeViewRequest):
			self.InitializeWindow(event.ScreenSize)
			self.Mediator.Post(Events.InitializeViewResponse())
		if isinstance(event, Events.LoadLevelRequest):
			self.WorldScreen = pygame.Surface((event.Parameters.MapSize[0]*Constants.TILE_X, event.Parameters.MapSize[1]*Constants.TILE_Y)).convert()
			TileLoader = Assets.TileSetLoader()
			for tileName in self.TileSets.keys():
				if not tileName in event.Parameters.RequiredTilesets:
					del self.TileSets[tileName]

			for tileSet in event.Parameters.RequiredTilesets:
				if not tileSet in self.TileSets.keys():
					self.TileSets[tileSet] = TileLoader.LoadTileSet(tileSet)

			self.ViewState = ViewModel.ViewState(event.Parameters.MapSize, event.Parameters.StartingOffset, self.WorldSize)
			for view in event.Parameters.ViewEntities:
				self.ViewState.Entities = event.Parameters.ViewEntities
			self.State = Constants.VIEWSTATE_READY
		if isinstance(event, Events.UpdateViewEvent):
			self.State = Constants.VIEWSTATE_RUNNING
			self.ViewState.ApplyUpdates(event.Updates)
		if isinstance(event, Events.ShiftOffsetEvent):
			self.ViewState.ShiftOffset(event.Delta)

			

		

