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
        costume2 = self.add_costume("images/robot_blue2.png")
        costume2.orientation = -90
        self.size = (99, 99)
        self.direction = "right"
        self.i = 0

    def act(self):
        j = 20
        self.i = self.i + 1
        if self.i > j:
            self.i = 0
        if self.i == j:
            print("switch costume", self.costume.orientation)
            self.switch_costume()



board = MyBoard()
board.show()
