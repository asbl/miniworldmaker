from miniworldmaker import *


class MyBoard(ProcessingBoard):

    def on_setup(self):
        self.add_image("images/backgroundColorGrass.png")
        print(self.background._image)
        self.physics_accuracy = 5
        self.background.fill((0, 0, 0, 255))
        self.line1 = Line((0, 100), (400, 900), 5)
        self.line1.physics.elasticity = 0.4
        self.line1._start_physics()
        #self.line2 = Line((50, 400), (300, 400),5)
        #self.line2.physics.elasticity = 0.4
        #self.line2._start_physics()
        self.circle1 = MyCircle((100,60), 10)
        self.line3 = Line((80, 150), (100, 200), 10)
        self.line3.physics.elasticity = 0.4
        self.line3._start_physics()
        print("line", self.line3, self.line3.start_position, self.line3.end_position)
        #self.box = Rectangle((300, 90), 80, 10,0)
        #self.box.costume.fill_color = (255,0,0,0)
        #self.box._start_physics()

class MyCircle(Circle):
    def on_setup(self):
        self.position = (70, 20)
        self.thickness = 0
        self.physics.elasticity = 0.8
        self.physics.mass = 10
        self._start_physics()



my_board = MyBoard(800, 600)
my_board.show()
