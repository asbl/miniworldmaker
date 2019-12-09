from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__()
        self.add_image("images/stone.jpg")


class Robot(Actor):
    def __init__(self):
        super().__init__()
        self.add_image("images/robo_green.png")


TiledBoard.register_token_type(Robot)
board = MyBoard.from_db("db_test.db")
board.show_log()
board.show()
