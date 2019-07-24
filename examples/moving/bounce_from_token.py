import random

from miniworldmaker import *


class MyBoard(PixelBoard):
    def __init__(self):
        super().__init__(160, 160)
        self.add_image("images/soccer_green.jpg")
        self.ball = SmallBall((10, 10))
        self.ball.direction = random.randint(0, 360)
        self.osbstacle = Obstacle((50, 50))


class SmallBall(Token):
    def __init__(self, position):
        super().__init__(position)
        self.size = (10, 10)
        self.add_image("images/ball_tennis.png")
        self.speed = 4

    def on_sensing_obstacle(self, other):
        self.move_back()
        self.board_connector.bounce_from_token(other)

    def on_sensing_borders(self, border):
        self.move_back()
        print("on_sensing_border")
        self.bounce_from_border(border)

    def act(self):
        self.move()


class Obstacle(Actor):
    def __init__(self, position):
        super().__init__(position)
        self.add_image("images/ball_soccer.png")
        self.size = (80, 80)

board = MyBoard()
board.show()