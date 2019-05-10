from miniworldmaker import *
import random


class PongBoard(PixelBoard):
    def __init__(self):
        super().__init__(600, 400)
        self.background.fill_color = (0, 0, 0)
        self.player1 = Paddle("left", (10, 130))
        self.player2 = Paddle("right", (580, 330))
        self.ball = Ball((395,295))
        self.ball.direction = 100

    def get_event(self, event, data):
        if event == "key_pressed":
            if "W" in data:
                self.player1.move_in_direction("up")
            if "S" in data:
                self.player1.move_in_direction("down")
            if "U" in data:
                self.player2.move_in_direction("up")
            if "J" in data:
                self.player2.move_in_direction("down")


class Paddle(Actor):
    def __init__(self, border, position):
        super().__init__(position)
        self.size = (10, 80)
        self.costume.fill_color = (255,255,255)
        self.costume.is_rotatable = False
        self.speed = 5
        self.border = border


class Ball(Actor):

    def __init__(self, position):
        super().__init__(position)
        self.size = (10, 10)
        self.costume.fill_color = (255, 255, 255)
        self.speed = 10

    def act(self):
        self.move()
        paddle = self.sensing_token(token = Paddle)
        if paddle:
            self.bounce_from_border(paddle.border)
            hit_pos = 40 + paddle.y - self.y
            self.turn_left(hit_pos)
            self.speed = 10 + abs(hit_pos) / 4
        borders = self.sensing_borders()
        if borders:
            self.bounce_from_border(borders)


board = PongBoard()
board.show()
