from miniworldmaker import *
import random


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(tile_size=100, columns=6, rows=6, tile_margin=1)
        self.add_to_board(Ship(), (1, 1))
        self.add_image("images/galaxy.jpg")
        event_console = EventConsole()
        self.window.add_container(event_console, dock="right", size=400)
        self.window.add_container(ActionBar(self), dock="bottom")
        actor_toolbar = ActiveActorToolbar()
        self.window.add_container(actor_toolbar, dock="right", size=400)

    def get_event(self, event, data):
        pass


class Ship(Actor):

    def __init__(self):
        super().__init__()
        self.spinning = 0
        self.add_image("images/ship.png")
        self.costume.orientation = 270

    def get_event(self, event, data):
        if event == "key_down":
            if "W" in data:
                self.direction = "up"
            elif "S" in data:
                self.direction = "down"
            elif "A" in data:
                self.direction = "left"
            elif "D" in data:
                self.direction = "right"

    def act(self):
        self.move()


board = MyBoard()

board.show()
