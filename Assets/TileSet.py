import pygame

class TileSet:
    def __init__(self, tileSheet, tileConfigs):
        self.TileSheet = tileSheet
        self.TileConfigs = tileConfigs

    def GetTileSurfaceByName(self, name):
        Tile = self.TileConfigs[name]
        Image = pygame.Surface([Tile['W'], Tile['H']]).convert()
        Image.blit(self.TileSheet, (0,0), (Tile['X'], Tile['Y'], Tile['W'], Tile['H']))
        return Image

    def BlitOnSurface(self, surface, drawable):
        Tile = self.TileConfigs[drawable.TileID]
        TileSetSection =  (Tile['X'], Tile['Y'], Tile['W'], Tile['H'])
        surface.blit(self.TileSheet, drawable.WorldLocation, TileSetSection)

    def BlitTileOnSurfaceByName(self, surface, name, location):
        Tile = self.TileConfigs[name]
        surface.blit(self.TileSheet, location, (Tile['X'], Tile['Y'], Tile['W'], Tile['H']))

    def GetTileSurfaceByLocation(self, x, y, w, h):
        image = pygame.Surface([w, h]).convert()
        image.blit(self.TileSheet, (0,0), (x,y,w,h))
        return image
