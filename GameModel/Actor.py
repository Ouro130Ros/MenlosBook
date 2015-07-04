from Entity import Entity

class Actor(Entity):
    def __init__(self, layer, tile_set, tile_id, parameters):
        super(Actor, self).__init__(layer, tile_set, tile_id)
        self.Hitpoints = parameters["Stats"]["HP"]
        self.Strength = parameters["Stats"]["STR"]
        self.EnergyCap = parameters["Stats"]["EnergyCap"]
        self.CurrentEnergy = parameters["Stats"]["EnergyCap"]
        self.Speed = parameters["MoveSpeed"]
        self.NextAction = None
        self.State = None

    def AddEnergy(self, energy):
        self.CurrentEnergy += energy
        if self.CurrentEnergy > self.EnergyCap: self.CurrentEnergy = self.EnergyCap

    def CanMove(self):
        return self.CurrentEnergy == self.EnergyCap

    def GetNextAction(self, actors, locations):
        pass
