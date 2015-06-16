import pygame
from TileSet import TileSet
import json
import os

class TileSetLoader:
	def LoadTileSet(self, tileSetName):
		BaseLocation = os.getcwd() + '//Gfx//' + tileSetName
		try:
			TileSheet = pygame.image.load(BaseLocation + '.png')
		except pygame.error, message:
			raise #TODO

		try:
			with open(BaseLocation + '.json') as DataFile:
				Parameters = json.load(DataFile)
		except Exception, e:
			raise #TODO

		return TileSet(TileSheet, Parameters)

