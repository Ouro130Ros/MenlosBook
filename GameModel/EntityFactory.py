from Entity import Entity
from StaticEntity import StaticEntity
from Player import Player
from Rat import Rat

class EntityFactory:
    def GetEntity(self, entityConfig, layer):
        if entityConfig.EntityType == "Static":
            return StaticEntity(layer, entityConfig.TileSet, entityConfig.TileID, entityConfig.Parameters)
        if entityConfig.EntityType == "Player":
            return Player(layer, entityConfig.TileSet, entityConfig.TileID, entityConfig.Parameters)
        if entityConfig.EntityType == "Rat":
            return Rat(layer, entityConfig.TileSet, entityConfig.TileID, entityConfig.Parameters)
        else:
            return Entity(layer, entityConfig.TileSet, entityConfig.TileID)