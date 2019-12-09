from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(tile_size=50, columns=10, rows=1, tile_margin=1)
        player1 = Fish((0, 0))
        self.add_image("images/water.png")


class Fish(Actor):

    def on_setup(self):
        self.add_image(path="images/fish.png")
        self.costume.orientation = - 90
        self.direction = "right"

    def act(self):
        self.move()

    def on_sensing_not_on_board(self):
        self.move_back()
        self.flip_x()

board = MyBoard()
board.show()
