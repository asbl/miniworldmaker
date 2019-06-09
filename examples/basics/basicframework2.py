from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(columns=20, rows=8, tile_size=42, tile_margin=0)
        self.rounds = 1
        self.counter = TextToken(position=(4,3), text=str(self.rounds))
        self.counter.size = (160,160)
        player1 = Player(position=(3, 3))
        self.add_image(path="images/stone.png")
        self.background.is_scaled_to_tile= True
        self.background.is_textured = True
        self.background.grid_overlay = True
        self.window.add_container(ActionBar(self), dock = "bottom")


class Player(Actor):

    def __init__(self, position):
        super().__init__(position)
        self.add_image(path="images/char_blue.png")
        self.costume.orientation = - 90

    def act(self):
        if not self.sensing_on_board(distance = 1):
            self.turn_left(90)
        if self.position == (0,0):
            self.board.rounds += 1
            self.board.counter.set_text(str(self.board.rounds))
        self.move()


board = MyBoard()
board.show()

