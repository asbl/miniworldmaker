from miniworldmaker import *


class MyBoard(TiledBoard):

    def on_setup(self):
        self.tile_size = 60
        self.player = Player(position=(1, 1))
        self.add_image(path="images/soccer_green.jpg")
        self.background.is_scaled = True
        self.speed = 10
        print(self.is_running)


class Player(Actor):

    def on_setup(self):
        self.add_image(path="images/char_blue.png")
        self.costume.is_upscaled = True
        self.costume.orientation = - 90

    def act(self):
        if self.sensing_on_board(1):
            self.move()

    def on_key_down_w(self):
        self.direction = "up"

    def on_key_down_s(self):
        self.direction = "down"

    def on_key_down_a(self):
        self.direction = "left"

    def on_key_down_d(self):
        self.direction = "right"


board = MyBoard(6, 4)
board.show()
