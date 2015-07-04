import Events
import Controllers

def main():
    mediator = Events.EventMediator()

    console = Controllers.ConsoleController(mediator)
    game = Controllers.GameController(mediator)
    input = Controllers.InputController(mediator)
    paceMaker = Controllers.PacemakerController(mediator)
    view = Controllers.ViewController(mediator)

    paceMaker.Run()

if __name__ == '__main__':
    main()
