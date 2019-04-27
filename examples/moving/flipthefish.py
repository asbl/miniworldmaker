from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(tile_size=50, columns=10, rows=1, tile_margin=1)
        player1 = Player()
        self.add_to_board(player1, position=(0, 0))
        self.add_image("images/water.png")


class Player(Actor):

    def __init__(self):
        super().__init__()
        self.add_image(path="images/fish.png")
        self.costume.orientation = - 90
        self.direction = "right"

    def act(self):
        if self.sensing_on_board():
            self.move()
        else:
            self.flip_x()


board = MyBoard()
board.show()
