from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(columns=20, rows=8, tile_size=42, tile_margin=1)
        player1 = Player( )
        self.add_actor(player1, position=(3, 3))
        player2 = Player()
        self.add_actor(player2, position=(8, 2))
        self.add_image(path="images/soccer_green.jpg")
        player3 = Player()
        self.add_actor(player3, position=(1, 1))


class Player(Actor):

    def __init__(self):
        super().__init__()
        self.add_image(path="images/char_blue.png")

    def act(self):
        if not self.board.on_board(self.look_forward()):
            self.turn_left(90)
        self.move()


board = MyBoard()
board.speed = 40
board.show()

