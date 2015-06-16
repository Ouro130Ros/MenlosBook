import pygame
from Controller import Controller
from Events import *
import Constants
from Models import Tileset
import json
import os

class AssetController(Controller):
	def __init__(self, mediator):
		super(AssetController, self).__init__(mediator)
		self.AssetState = Constants.ASSET_STATE_OPEN
		
	def RetrieveAsset(self, request):
		if request.AssetType == Constants.ASSET_TYPE_TILESET:
			AssetBase = os.getcwd()  + '\\Gfx\\' + request.AssetLocation
			try:
				Sheet = pygame.image.load(AssetBase + '.png')
			except pygame.error, message:
				self.Mediator.Post(AssetRetrieveFailedEvent(request.RequestID, str(message)))
				return
			try:
				with open(AssetBase + '.json') as datafile:
					Parameters = json.load(datafile)
			except Exception, m:
				print m
				self.Mediator.Post(AssetRetrieveFailedEvent(request.RequestID, "Failed to find tile definitions at: " + AssetBase + '.json'))
				return
			
			self.Mediator.Post(AssetResponseEvent(request.RequestID, Constants.ASSET_TYPE_TILESET, Tileset(Sheet, Parameters)))
				
	def Notify(self, event):
		if self.AssetState == Constants.ASSET_STATE_OPEN:
			if isinstance(event, AssetRequestEvent):
				self.AssetState = Constants.ASSET_STATE_BUSY
				self.Mediator.Post(AssetRequestRecievedEvent(event.RequestID))
				self.RetrieveAsset(event)
				self.AssetState = Constants.ASSET_STATE_OPEN

				
			