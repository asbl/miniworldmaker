from miniworldmaker import *
import random


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(tile_size=100, columns=6, rows=6, tile_margin=1)
        self.add_to_board(Ship(), (1, 1))
        self.add_image("images/galaxy.jpg")
        event_console = EventConsole()
        self.window.add_container(event_console, dock="right", size=400)
        event_console.register_events = {"actor_moved"}
        action_bar = ActionBar(self)
        self.window.add_container(action_bar, dock="bottom")
        actor_toolbar = TokenToolbar(self)
        self.window.add_container(actor_toolbar, dock="right", size=400)

    def get_event(self, event, data):
        print(self.active_token)

class Ship(Actor):

    def __init__(self):
        super().__init__()
        self.spinning = 0
        self.add_image("images/ship.png")
        self.orientation = 270

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
