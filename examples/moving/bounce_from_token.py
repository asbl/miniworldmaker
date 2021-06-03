import random

from miniworldmaker import *


class MyBoard(PixelBoard):
    def __init__(self):
        super().__init__(160, 160)
        self.add_background("images/soccer_green.jpg")
        self.ball = SmallBall((10, 10))
        self.ball.direction = random.randint(0, 360)
        self.osbstacle = Obstacle((50, 50))


class SmallBall(Token):
    def __init__(self, position):
        super().__init__(position)
        self.size = (10, 10)
        self.add_costume("images/ball_tennis.png")
        self.speed = 4

    def on_sensing_obstacle(self, other):
        self.move_back()
        self.bounce_from_token(other)

    def on_sensing_borders(self, border):
        print(border)
        self.move_back()
        self.bounce_from_border(border)

    def act(self):
        self.move()


class Obstacle(Token):
    def __init__(self, position):
        super().__init__(position)
        self.add_costume("images/ball_soccer.png")
        self.size = (80, 80)

board = MyBoard()
board.run()
