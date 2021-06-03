from miniworldmaker import *


class MyBoard(PixelBoard):

    def __init__(self):
        super().__init__(columns=280, rows=100)
        self.add_background("images/water.png")
        player1 = Robot(position=(0, 0))
        self.speed = 1


class Robot(Token):

    def setup(self):
        self.add_costume()
        self.costume.add_images(["images/1.png", "images/2.png","images/3.png","images/4.png"])
        self.size = (99, 99)
        self.costume.animation_speed = 120
        self.costume.is_animated = True
        self.costume.orientation = - 90
        self.direction = "right"

    def act(self):
        if self.sensing_on_board():
            self.move()

    def on_sensing_not_on_board(self):
        self.flip_x()
        self.move()


board = MyBoard()
board.run()
