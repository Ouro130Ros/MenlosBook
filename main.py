import pygame
import Events
import Controllers

def Main():
	Mediator = Events.EventMediator()

	Console = Controllers.ConsoleController(Mediator)
	Game = Controllers.GameController(Mediator)
	Input = Controllers.InputController(Mediator)
	PaceMaker = Controllers.PacemakerController(Mediator)
	View = Controllers.ViewController(Mediator)

	PaceMaker.Run()	

if __name__ == '__main__':
	Main()
