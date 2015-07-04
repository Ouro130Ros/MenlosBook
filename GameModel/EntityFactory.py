from Entity import Entity
from StaticEntity import StaticEntity
from Player import Player
from Rat import Rat

class EntityFactory:
    def GetEntity(self, entity_config, layer):
        if entity_config.EntityType == "Static":
            return StaticEntity(layer, entity_config.TileSet, entity_config.TileID, entity_config.Parameters)
        if entity_config.EntityType == "Player":
            return Player(layer, entity_config.TileSet, entity_config.TileID, entity_config.Parameters)
        if entity_config.EntityType == "Rat":
            return Rat(layer, entity_config.TileSet, entity_config.TileID, entity_config.Parameters)
        else:
            return Entity(layer, entity_config.TileSet, entity_config.TileID)