from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(tile_size=50, columns=4, rows=1, tile_margin=1)
        player1 = Fish((0, 0))
        self.add_background("images/water.png")
        self.speed = 20


class Fish(Token):

    def on_setup(self):
        self.add_costume("images/fish.png")
        self.costume.orientation = - 90
        self.direction = "right"

    def act(self):
        print("act", self.position, self.direction)
        self.move()

    def on_sensing_not_on_board(self):
        print("move back")
        self.move_back()
        print("flip x")
        self.flip_x()
        

board = MyBoard()
board.run()
