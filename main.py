import pygame
from Events import *
from Controllers import *

def Main():
	Mediator = EventMediator()

	Console = ConsoleController(Mediator)
	Game = GameController(Mediator)
	Input = InputController(Mediator)
	PaceMaker = PacemakerController(Mediator)
	View = ViewController(Mediator)

	PaceMaker.Run()	

if __name__ == '__main__':
	Main()
