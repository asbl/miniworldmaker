from miniworldmaker import *


class PongBoard(PhysicsBoard):

    def on_setup(self):
        self.debug = True
        self.add_background((100, 0, 0, 255))
        self.damping = 1
        self.gravity = 0, 0
        self.player1 = Paddle((10, 130), width=10, height=80, thickness=0)
        self.player2 = Paddle((740, 280), width=10, height=80, thickness=0)
        self.left = Border((0, 0), (0, 600), 1)
        self.top = Border((0, 0), (800, 0), 1)
        self.right = Border((795, 0), (795, 600), 1)
        self.bottom = Border((0, 595), (800, 595), 1)
        self.points_left = NumberToken((100, 100), 0, 100)
        self.points_left.size = (200, 200)
        self.points_left.physics.simulation = None
        self.points_right = NumberToken((600, 100), 0, 100)
        self.points_right.size = (200, 200)
        self.points_right.costume._reload_all()
        self.points_right.costume.dirty = 1
        self.points_right.physics.simulation = None
        self.ball = Ball((295, 5))

    def on_key_pressed_w(self):
        self.player1.move_in_direction("up")

    def on_key_pressed_s(self):
        self.player1.move_in_direction("down")

    def on_key_pressed_u(self):
        self.player2.move_in_direction("up")

    def on_key_pressed_j(self):
        self.player2.move_in_direction("down")


class Border(Line):

    def on_setup(self):
        self.physics.friction = 0
        self.physics.elasticity = 1
        self.physics.simulation = "manual"


class Paddle(Rectangle):
    def on_setup(self):
        self.size = (10, 80)
        self.costume.is_rotatable = False
        self.physics.simulation = "manual"     
        self.physics.friction = 0
        self.physics.elasticity = 1
        

class Ball(Circle):

    def on_setup(self):
       self.add_costume("images/fly.png")
       self.direction = 30
       self.size = (30,30)
       self.position = (400,200)
       self.physics.mass = 1
       self.physics.elasticity = 1
       self.physics.friction = 0

       
    def on_begin_simulation(self):
       self.impulse(160, 2500)
       
    def on_touching_line(self, line, collision):
        print("touching line ", line, collision, self.board.left)
        if line == self.board.left:
            print("inc points")
            self.board.points_right.inc()
        if line == self.board.right:
            self.board.points_left.inc()

board = PongBoard(800, 600)
board.run()
