from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self, rows, columns):
        super().__init__()
        self.add_image("images/stone.jpg")


class Robot(Actor):
    def __init__(self):
        super().__init__()
        self.add_image("images/robo_green.png")


print("globals in main", globals())
class_lookup = [(c, globals()[c]) for c in dir() if hasattr(globals()[c], "lookup")]
TiledBoard.register_token_type(Robot)
board = MyBoard.from_db("db_test.db")
board.show_log()
board.show()
