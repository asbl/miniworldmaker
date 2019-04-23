from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(columns=20, rows=8, tile_size=42, tile_margin=0)
        player1 = Player( )
        self.add_to_board(player1, position=(3, 3))
        player2 = Player()
        self.add_to_board(player2, position=(8, 2))
        self.add_image(path="images/stone.png")
        self.background.is_scaled_to_tile= True
        self.background.is_textured = True
        self.background.grid_overlay = True
        player3 = Player()
        self.add_to_board(player3, position=(0, 1))
        self.window.add_container(ActionBar(self), dock = "bottom")


class Player(Actor):

    def __init__(self):
        super().__init__()
        self.add_image(path="images/char_blue.png")
        # self.costume.show_info_overlay((0,100,255))

    def act(self):
        if not self.sensing_on_board(distance = 1):
            self.turn_left(90)
        self.move()
        print(self.direction)


board = MyBoard()
board.show()

