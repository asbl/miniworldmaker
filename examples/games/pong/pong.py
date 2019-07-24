from miniworldmaker import *


class PongBoard(PixelBoard):
    def __init__(self):
        super().__init__(800, 600)
        self.background.fill_color = (0, 0, 0)
        self.player1 = Paddle("left", (10, 130))
        self.player2 = Paddle("right", (780, 130))
        self.ball = Ball((395,295))
        self.ball.direction = 100

        self.physics_property.damping = 1
        self.lines = [Line((0, 0), (0, 600), 5),
                      Line((0, 0), (800, 0), 5),
                      Line((800, 600), (800, 0), 5),
                      Line((800, 600), (0, 600), 5),
                      ]

        for line in self.lines:
            line.physics.friction = 0
            line.physics.mass = 0
            line.physics.elasticity = 1
            line.start_physics()

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
        self.physics.gravity = False
        self.physics.elasticity = 1
        self.start_physics()


class Ball(Circle):

    def __init__(self, position):
        super().__init__(position, 5, 0)
        self.color = (255, 255, 255)
        self.speed = 5
        self.physics.gravity = False
        self.physics.mass = 1000
        self.physics.elasticity = 1
        self.start_physics()
        self.physics.velocity_x = 500
        self.physics.velocity_y = 200


board = PongBoard()
board.show()
