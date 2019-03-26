from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(columns=4, rows=4)
        self.tile_size = 40
        self.add_image("images/stone.jpg")
        self.add_to_board(Robot(), (2, 2))
        self.add_to_board(Robot(), (3, 3))


class Robot(Actor):
    def __init__(self):
        super().__init__()
        self.add_image("images/robo_green.png")


board = MyBoard()
board.save_to_db("db_test.db")
board.show()
