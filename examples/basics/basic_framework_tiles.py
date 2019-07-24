from miniworldmaker import *


class MyBoard(TiledBoard):

    def on_setup(self):
        self.add_image(path="images/stone.png")
        self.background.is_textured = True
        self.background.is_scaled_to_tile = True
        self.player = Player(position=(3, 4))


class Player(Actor):

    def on_setup(self):
        self.add_image(path="images/char_blue.png")
        self.costume.orientation = - 90

    def key_down(self, keys):
        if "A" in keys:
            self.turn_left()
        if "D" in keys:
            self.turn_right()
        if "W" in keys:
            self.move()
        if not self.sensing_on_board(distance=0):
            self.move(-1)


board = MyBoard(columns=20, rows=8, tile_size=42)
board.show()
