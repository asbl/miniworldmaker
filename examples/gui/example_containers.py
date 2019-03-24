from miniworldmaker import *
import random


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(tile_size=100, columns=6, rows=6, tile_margin=1)
        self.add_to_board(Ship(), (1, 1))
        self.add_image("images/galaxy.jpg")


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
eventConsole = EventConsole()
board.window.add_container(eventConsole, dock="right", size=600)
eventConsole = ActionBar(board)
board.window.add_container(eventConsole, dock="bottom")
board.show()
