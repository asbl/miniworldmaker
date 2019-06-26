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

    def act(self):
        pass


class Arrow(Actor):
    def on_setup(self):
        self.size = (30,30)
        self.costume.add_image("images/tank_arrowFull.png")
        self.costume.enable_action("scale")
        self.speed = 0
        self.shoot = 0

    def get_event(self, event, data):
        if event == "key_pressed":
            if "w" in data:
                self.direction -= 1
                #self.y -= 1
            elif "s" in data:
                self.direction += 1
               # self.y += 1
            elif "space" in data:
                self.speed += 1
                self.shoot = 1
        elif event == "key_up":
            if self.shoot == 1:
                self.shoot = -1
                print("Bäm")
                Bird(position=self.position)
                self.speed = 0


class Plattform(Token):

    def on_setup(self):
        self.physics.gravity = False
        self.physics.can_move = False
        self.stable = True
        self.physics.friction = 0.5
        self.add_image("images/stone.png")
        self.size = (256, 64)
        self.costume.is_textured = True
        self.costume.enable_action("textured")
        self.start_physics()



class Box(Actor):

    def on_setup(self):
        self.add_image("images/box_blue.png")
        self.size = (40, 40)
        self.physics.friction = 0.1
        self.start_physics()


class Bird(Actor):

    def on_setup(self):
        self.add_image("images/fly.png")
        self.costume.orientation = 180
        self.flip_x()
        self.size = (80, 80)
        self.mass = 20
        self.physics.size = 0.7, 0.7
        self.physics.shape_type = "circle"
        self.physics.stable = False
        self.start_physics()
        self.physics.velocity_x = 1500
        self.physics.velocity_y = - self.board.arrow.direction * 50

    def act(self):
        if "bottom" in self.sensing_borders() or "right" in self.sensing_borders():
            self.remove()


board = MyBoard(1024, 700)
board.show()