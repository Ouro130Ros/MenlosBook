from datetime import datetime
import Constants

class ViewState:
    def __init__(self, map_size, world_center, screen_size):
        self.MapSize = map_size
        self.ScreenSize = screen_size
        self.UpdateAll = False
        self.LastTimestamp = datetime.now()
        self.DrawFrame = True
        self.Entities = []
        self.Offset = [0,0]
        self.center_on_point(world_center)

    def add_entity(self, view_entity):
        self.Entities.append(view_entity)
        
    def get_drawable_updates(self):
        updates = []
        if self.UpdateAll:
            self.UpdateAll = False
            for e in self.Entities: updates.append(e.get_drawable())
        else:
            for e in self.Entities:
                if e.Update:
                    updates.append(e.get_drawable())
                    for u in e.EntitiesUnder:
                        updates.append(u.get_drawable())
        return sorted(updates, key=lambda x: x.Layer)
            
    def on_tick(self):
        currentTime = datetime.now()
        elapsedTime = (self.LastTimestamp - currentTime)
        elapsedMS = (elapsedTime.days * 24 * 60 * 60 + elapsedTime.seconds) * 1000 + elapsedTime.microseconds / 1000.0
        if elapsedMS > 42:
            self.DrawFrame = True

    def center_on_point(self, point):
        self.Offset = [0, 0]
        self.shift_offset(((point[0]*Constants.TILE_X) - (self.ScreenSize[0]/2),
                          (point[1]*Constants.TILE_Y) - (self.ScreenSize[0]/2)))

    def is_ready(self):
        for e in self.Entities: 
            if e.Update: return False
        return True

    def shift_offset(self, delta):
        self.Offset[0] += delta[0]
        self.Offset[1] += delta[1]
        if self.Offset[0] < 0: self.Offset[0] = 0
        if self.Offset[1] < 0: self.Offset[1] = 0
        if self.Offset[0] > (self.MapSize[0]*Constants.TILE_X) - self.ScreenSize[0]:
            self.Offset[0] = (self.MapSize[0]*Constants.TILE_X) - self.ScreenSize[0]
        if self.Offset[1] > (self.MapSize[1]*Constants.TILE_Y) - self.ScreenSize[1]:
            self.Offset[1] = (self.MapSize[1]*Constants.TILE_Y) - self.ScreenSize[1]
    
    def apply_updates(self, updates):
        deleteEntities = list()
        for entity in updates:
            entity.Update = True
            for existingEntity in self.Entities:
                if existingEntity.ModelEntityID == entity.ModelEntityID:
                    deleteEntities.append(existingEntity)
                    
        for delete in deleteEntities:
            if delete in self.Entities:
                self.Entities.remove(delete)

        self.Entities = self.Entities + updates
