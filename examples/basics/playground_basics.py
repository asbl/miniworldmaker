from miniworldmaker import *


class MyBoard(TiledBoard):

    def setup(self):
        self.columns = 20
        self.rows = 8
        self.tile_size = 42
        self.add_image(path="images/soccer_green.jpg")
        self.background.grid_overlay = True
        player1 = Player(position=(3, 3))


class Player(Actor):

    def setup(self):
        self.add_image(path="images/char_blue.png")

board = MyBoard()
board.show()