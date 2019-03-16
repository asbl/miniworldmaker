from miniworldmaker import *


class MyBoard(TileBasedBoard):

    def __init__(self):
        super().__init__(columns=20, rows=8, tile_size=42, tile_margin=1)
        player1 = Player()
        self.add_actor(player1, position=(1, 1))
        self.add_image(path="images/soccer_green.jpg")


class Player(Actor):

    def __init__(self):
        super().__init__()
        self.size = (40, 40)
        self.add_image(path="images/char_blue.png")

    def act(self):
        if self.grid.is_in_grid(self.look_forward()):
            self.move()

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


board = MyBoard()
board.speed = 50
board.show()
