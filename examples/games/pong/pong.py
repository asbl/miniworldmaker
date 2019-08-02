from miniworldmaker import *


class PongBoard(PixelBoard):

    def on_setup(self):
        self.background.fill_color = (100, 0, 0)
        self.player1 = Paddle((10, 130), width=10, height=80, thickness=0)
        self.player2 = Paddle((780, 280), width=10, height=80, thickness=0)
        self.ball = Ball((395, 295))
        self.physics_property.damping = 1
        self.left = Border((0, 0), (0, 600), 5)
        self.top = Border((0, 0), (800, 0), 5)
        self.right = Border((795, 600), (795, 0), thickness=10)
        self.bottom = Border((800, 595), (0, 595), 5)
        self.points_left = NumberToken((100, 100), 0, 100)
        self.points_left.size = (200, 200)
        self.points_right = NumberToken((600, 100), 0, 100)
        self.points_right.size = (200, 200)

    def on_key_pressed(self, keys):
        if "W" in keys:
            self.player1.move_in_direction("up")
        if "S" in keys:
            self.player1.move_in_direction("down")
        if "U" in keys:
            self.player2.move_in_direction("up")
        if "J" in keys:
            self.player2.move_in_direction("down")


class Border(Line):

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

    def on_sensing_collision_with_border(self, line, collision):
        if line == self.board.left:
            self.board.points_right.inc()
        if line == self.board.right:
            self.board.points_left.inc()

board = PongBoard(800, 600)
board.show(fullscreen=False)
