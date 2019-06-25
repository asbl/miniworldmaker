from miniworldmaker import *


class MyBoard(ProcessingBoard):

    def __init__(self, width, height):
        super().__init__(width, height)


    def on_setup(self):
        self.add_image("images/backgroundColorGrass.png")
        print(self.background._image)
        self.physics_accuracy = 5
        self.fill((0, 0, 0, 255))
        self.line1 = Line((0, 100), (600, 800), 5)
        self.line1.physics.elasticity = 0.4
        self.line1.start_physics()
        self.line2 = Line((50, 400), (300, 400),5)
        self.line2.physics.elasticity = 0.4
        self.line2.start_physics()
        self.circle = Circle((70, 20), 5, 0)
        self.circle.physics.elasticity = 0.8
        self.circle.physics.mass = 10
        self.circle.start_physics()
        self.circle.set_token_mode()
        self.line3 = Line((0, 350), (600, 400), 10)
        self.line3.physics.elasticity = 0.4
        self.line3.start_physics()
        self.box = Rectangle((300, 90), 80, 80, 0)
        self.box.image.fill((90, 255, 0, 220))
        self.box.physics.stable = False
        self.box.start_physics()
        #self.physics_property.debug = False

    def act(self):
        pass

my_board = MyBoard(800, 600)
my_board.show()
