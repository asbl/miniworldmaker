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

    def act(self):
        if self.is_looking_on_board():
            self.move()
        else:
            self.flip_x()


board = MyBoard()
board.speed = 50
board.show()
