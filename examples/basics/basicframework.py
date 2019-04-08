from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(columns=20, rows=8, tile_size=42, tile_margin=0)
        player1 = Player( )
        self.add_to_board(player1, position=(3, 3))
        player2 = Player()
        self.add_to_board(player2, position=(8, 2))
        self.add_image(path="images/soccer_green.jpg")
        player3 = Player()
        self.add_to_board(player3, position=(1, 1))
        self.window.add_container(ActionBar(self), dock = "bottom")
        self.background.show_grid()

class Player(Actor):

    def __init__(self):
        super().__init__()
        self.add_image(path="images/char_blue.png")

    def act(self):
        #if not self.sensing_on_board():
        #    self.turn_left(90)
        self.direction = 0
        self.move()


board = MyBoard()
board.show()

