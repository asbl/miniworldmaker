from miniworldmaker import *


class MyBoard(TiledBoard):

    def setup(self):
        self.columns = 20
        self.rows = 10
        self.tile_size = 5
        self.add_image(path="images/backgroundColorGrass.png")

board = MyBoard()
board.show()