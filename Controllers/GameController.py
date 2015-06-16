import Constants
from Controller import Controller
import Assets
import Events
from GameModel import GameStateManager

class GameController(Controller):
    def __init__(self, mediator):
      super(GameController, self).__init__(mediator)

      self.State = Constants.GAMESTATE_STARTUP
      self.Level = None
      self.Configuration = Assets.Configuration()

    def OnTick(self):
        if self.State == Constants.GAMESTATE_STARTUP: 
          self.Level = GameStateManager()
          self.Mediator.Post(Events.InitializeViewRequest(self.Configuration.GetWindowSize()))
          self.State = Constants.GAMESTATE_WAITINGONVIEW
        if self.State == Constants.GAMESTATE_LOADING_LEVEL:
          self.Level.LoadLevel(self.Configuration.GetLevel(self.Level.CurrentLevel))
          self.Mediator.Post(Events.LoadLevelRequest(self.Level.GetViewStateLevelParams()))
          self.State = Constants.GAMESTATE_WAITINGONVIEW
        if self.State == Constants.GAMESTATE_RUNNING:
          Updates = self.Level.OnTick()
          self.State = Constants.GAMESTATE_WAITINGONVIEW
          if len(Updates) > 0: self.Mediator.Post(Events.UpdateViewEvent(Updates))
                
    def Notify(self, event):
        if isinstance(event, Events.TickEvent):
          self.OnTick()
        if isinstance(event, Events.ViewReadyEvent):
          self.State = Constants.GAMESTATE_RUNNING
        if isinstance(event, Events.CharacterActionEvent):
          self.Level.ApplyCharacterInput(event.Command)
        if isinstance(event, Events.InitializeViewResponse):
          self.State = Constants.GAMESTATE_LOADING_LEVEL

                