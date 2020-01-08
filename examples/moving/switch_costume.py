from miniworldmaker import *


class MyBoard(PixelBoard):

    def __init__(self):
        super().__init__(columns=280, rows=100)
        self.add_image("images/water.png")
        player1 = Robot(position=(0, 0))
        self.speed = 1


class Robot(Actor):

    def __init__(self, position):
        super().__init__(position)
        self.add_image("images/robot_blue1.png")
        self.costume.orientation = - 90
        self.costume.animation_speed = 30
        self.costume.is_animated = True
        self.animation1 = ["images/robot_blue2.png", "images/robo_green.png", "images/robo_green.png"]
        self.size = (99, 99)
        self.direction = "right"
        self.i = 0
        self.costume.animate(self.animation1)

    def act(self):
        j = 150
        self.i = self.i + 1
        if self.i > j:
            self.i = 0
        if self.i == j:
            self.costume.animate(self.animation1)
            pass
        if self.sensing_on_board():
            self.move()

    def on_sensing_not_on_board(self):
        self.flip_x()
        self.move()


board = MyBoard()
board.show()
