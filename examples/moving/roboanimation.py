from miniworldmaker import *

class MyBoard(PixelBoard):

    def __init__(self):
        super().__init__(columns=280, rows=100)
        self.add_image("images/water.png")
        player1 = Robot(position=(0, 0))


class Robot(Actor):

    def __init__(self, position):
        super().__init__(position)
        self.add_image("images/robot_blue1.png")
        self.add_image("images/robot_blue2.png")
        self.size = (105, 105)
        self.costume.animation_speed = 30
        self.costume.is_animated = True
        self.costume.orientation = - 90
        self.direction = "right"

    def act(self):
        if self.sensing_on_board():
            self.move()
        else:
            self.flip_x()
            self.move()


board = MyBoard()
board.speed = 100
board.show()
