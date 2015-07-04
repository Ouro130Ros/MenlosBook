class Location:
    def __init__(self, location_xy):
        self.Location = location_xy #(x, y)
        self.Neighbors = [None, None, None, None]
        self.Entities = [] #Entity()
        
    def on_enter(self, entity):
        pass
    
    def on_exit(self, entity):
        pass

    def on_update(self, command_event):
        pass