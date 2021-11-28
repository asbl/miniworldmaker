from miniworldmaker import *


class MyBoard(TiledBoard):

    def on_setup(self):
        self.size = (4, 4)
        print(self.columns, self.rows, self.size)
        self.tile_size = 40
        self.add_background("images/stone.jpg")
        Robot((2, 2))
        Robot((3, 3))
        board.save_to_db("db_test.db")


class Robot(Token):
    def on_setup(self):
        self.add_costume("images/robo_green.png")


board = MyBoard()
board.run()
