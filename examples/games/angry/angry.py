from miniworldmaker import *


class MyBoard(PixelBoard):

    birds = 0

    def on_setup(self):
        self.background.add_image("images/backgroundColorGrass.png")
        self.arrow = Arrow(position=(160, 250))
        self.arrow.direction = -10
        self.plattform = Plattform(position=(600, 250))
        Box(position=(610, 210))
        Box(position=(655, 210))
        Box(position=(700, 210))
        Box(position=(745, 210))
        Box(position=(790, 210))

        Box(position=(630, 170))
        Box(position=(675, 170))
        Box(position=(720, 170))
        Box(position=(765, 170))

        Box(position=(640, 130))
        Box(position=(685, 130))
        Box(position=(730, 130))

        Box(position=(700, 90))


class Arrow(Actor):

    def on_setup(self):
        self.size = (30,30)
        self.costume.add_image("images/tank_arrowFull.png")
        self.costume.is_scaled = True
        self.speed = 0
        self.shoot = 0

    def on_key_pressed(self, keys):
        if "w" in keys:
            self.direction -= 1
        elif "s" in keys:
            self.direction += 1

    def on_key_down(self, keys):
        if "space" in keys:
            self.speed += 1
            self.shoot = 1
            if self.shoot == 1:
                self.shoot = -1
                print("Bäm")
                bird = Bird(position=self.position)
                self.speed = 0
                print(bird)


class Plattform(Token):

    def on_setup(self):
        self.add_image("images/stone.png")
        self.size = (256, 64)
        self.costume.is_textured = True

    def setup_physics(self):
        self.physics.gravity = False
        self.physics.can_move = False
        self.physics.friction = 0.5


class Box(Actor):

    def on_setup(self):
        self.add_image("images/box_blue.png")
        self.size = (40, 40)

    def setup_physics(self):
        self.physics.friction = 0.1


class Bird(Actor):

    def on_setup(self):
        self.add_image("images/fly.png")
        self.orientation = 180
        self.flip_x()
        self.size = (80, 80)
        self.physics.velocity_x = 600
        self.physics.velocity_y = - self.board.arrow.direction * 50

    def act(self):
        if "bottom" in self.sensing_borders() or "right" in self.sensing_borders():
            self.remove()

    def setup_physics(self):
        self.physics.mass = 20
        self.physics.size = 0.7, 0.7
        self.gravity = True
        self.physics.shape_type = "circle"
        self.physics.stable = False

board = MyBoard(1024, 700)
board.show()