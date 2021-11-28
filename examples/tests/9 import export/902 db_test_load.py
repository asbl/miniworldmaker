from miniworldmaker import *


class Robot(Token):
    def on_setup(self):
        self.add_costume("images/robo_green.png")


class MyBoard(TiledBoard):

    def on_setup(self):
        self.add_background("images/stone.jpg")
        board.load_tokens_from_db("db_test.db", [Robot])
        
board = MyBoard()
board = board.load_board_from_db("db_test.db")

board.run()
