from miniworldmaker import *
import random


class MyBoard(PixelBoard):
    def __init__(self):
        super().__init__(160, 160)
        self.add_image("images/soccer_green.jpg")
        self.ball = SmallBall((10, 10))
        self.ball.direction = random.randint(0, 360)
        self.osbstacle = Obstacle((50, 50))


class SmallBall(Actor):
    def __init__(self, position):
        super().__init__(position)
        self.size = (10, 10)
        self.add_image("images/ball_tennis.png")
        self.speed = 4

    def act(self):
        obstacle = self.sensing_token(token = Obstacle, exact=True)
        if obstacle:
            self.bounce_from_token(obstacle)
        borders = self.sensing_borders()
        if borders:
            self.bounce_from_border(borders)
        self.move()


class Obstacle(Actor):
    def __init__(self, position):
        super().__init__(position)
        self.add_image("images/ball_soccer.png")
        self.size = (80, 80)

board = MyBoard()
board.show()