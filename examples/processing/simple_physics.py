from miniworldmaker import *


class MyBoard(ProcessingBoard):

    def on_setup(self):
        self.physics_accuracy = 5
        self.fill((0, 0, 0, 255))
        self.line1 = Line((0, 100), (600, 800), 5)
        self.line1.physics.elasticity = 0.4
        self.line2 = Line((50, 400), (300, 400),5)
        self.line2.physics.elasticity = 0.4
        self.circle = Circle((70, 20), 5, 0)
        self.circle.physics.elasticity = 0.8
        self.circle.physics.mass = 10
        self.line3 = Line((0, 350), (600, 400), 10)
        self.line3.physics.elasticity = 0.4
        self.box = Rectangle((300, 90), 80, 80, 0)
        self.box.image.fill((90, 255, 0, 220))
        self.box.physics.stable = False
        self.line3.physics.elasticity = 0.4
        self.start_physics()
        #self.physics_property.debug = False

    #def act(self):
    #    self.line3.direction += 1

my_board = MyBoard(800, 600)
my_board.show()
