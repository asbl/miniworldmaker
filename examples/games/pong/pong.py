from miniworldmaker import *


class PongBoard(PixelBoard):

    def on_setup(self):
        self.add_background((100, 0, 0, 255))
        self.player1 = Paddle((10, 130), width=10, height=80, thickness=0)
        self.player2 = Paddle((780, 280), width=10, height=80, thickness=0)
        self.ball = Ball((395, 295))
        self.physics_property.damping = 1
        self.left = Line((0, 0), (0, 600), 5)
        self.top = Line((0, 0), (800, 0), 5)
        self.right = Line((795, 600), (795, 0), thickness=10)
        self.bottom = Line((800, 595), (0, 595), 5)
        self.points_left = NumberToken((100, 100), 0, 100)
        self.points_left.size = (200, 200)
        self.points_right = NumberToken((600, 100), 0, 100)
        self.points_right.size = (200, 200)

    def on_key_pressed_w(self):
        self.player1.move_in_direction("up")

    def on_key_pressed_s(self):
        self.player1.move_in_direction("down")

    def on_key_pressed_u(self):
        self.player2.move_in_direction("up")

    def on_key_pressed_j(self):
        self.player2.move_in_direction("down")


class Line(Line):

    def setup_physics(self):
        self.physics.mass = 1
        self.physics.elasticity = 1


class Paddle(Rectangle):
    def setup(self):
        self.size = (10, 80)
        self.costume.is_rotatable = False

    def setup_physics(self):
        self.physics.stable = True
        self.physics.can_move = True
        self.physics.mass = "inf"
        self.physics.friction = 0
        self.physics.gravity = False
        self.physics.elasticity = 1
        self.physics.shape_type = "rect"


class Ball(Circle):

    def on_setup(self):
        self.direction = 30
        self.physics.impulse_in_direction(300)

    def setup_physics(self):
        self.physics.mass = 1
        self.physics.elasticity = 1
        self.physics.friction = 0
        self.physics.shape_type = "circle"
        self.physics.gravity = False
        self.physics.stable = False

    def on_touching_line(self, line, collision):
        if line == self.board.left:
            self.board.points_right.inc()
        if line == self.board.right:
            self.board.points_left.inc()

board = PongBoard(800, 600)
board.run()
