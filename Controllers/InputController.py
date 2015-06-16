from Controller import Controller
import pygame
import Events
import Constants
import UserInput


class InputController(Controller):
	def __init__(self, mediator):
		super(InputController, self).__init__(mediator)
		self.InputState = Constants.INPUTSTATE_OPEN
		self.LastMousePos = None
		
	def Notify(self, event):
		if isinstance(event, Events.TickEvent):
			for pgEvent in pygame.event.get():
				ev = None
				if pgEvent.type == pygame.QUIT:
					ev = Events.QuitEvent()
				else:
					ev = self.ProcessPyGameEvent(pgEvent)
				if ev:
					self.Mediator.Post(ev)
					
	def ProcessPyGameEvent(self, pgEvent):
		if self.InputState == Constants.INPUTSTATE_OPEN:
			if pgEvent.type == pygame.KEYDOWN:
				if pgEvent.key == pygame.K_ESCAPE:
					return Events.QuitEvent()
				else:
					if pgEvent.key == pygame.K_UP:
						return Events.CharacterActionEvent(UserInput.MovementInput(Constants.DIRECTION_N))
					elif pgEvent.key == pygame.K_DOWN:
						return Events.CharacterActionEvent(UserInput.MovementInput(Constants.DIRECTION_S))
					elif pgEvent.key == pygame.K_LEFT:
						return Events.CharacterActionEvent(UserInput.MovementInput(Constants.DIRECTION_W))
					elif pgEvent.key == pygame.K_RIGHT:
						return Events.CharacterActionEvent(UserInput.MovementInput(Constants.DIRECTION_E))
			if pgEvent.type == pygame.MOUSEBUTTONDOWN:
				self.InputState = Constants.INPUTSTATE_MOUSEDOWN
				x, y = pgEvent.pos
				self.LastMousePos = (x, y)
		if self.InputState == Constants.INPUTSTATE_MOUSEDOWN:
			if pgEvent.type == pygame.MOUSEMOTION:
				x, y = pgEvent.pos
				Delta = (self.LastMousePos[0] - x, self.LastMousePos[1] - y)
				self.LastMousePos = (x,y)
				self.Mediator.Post(Events.ShiftOffsetEvent(Delta))
			if pgEvent.type == pygame.MOUSEBUTTONUP:
				self.InputState = Constants.INPUTSTATE_OPEN


		return None