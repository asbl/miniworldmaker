from miniworldmaker import *


my_board = PhysicsBoard(800, 600)
my_board.add_background((0, 0, 0, 255))

# line 1
line1 = Line((0, 100), (400, 900), 5, color=(100, 100, 255))
@line1.register
def setup_physics(self):
    self.physics.elasticity = 0.4

# line 2
line2 = Line((50, 400), (300, 400),5, color=(255, 0, 0))
@line2.register
def setup_physics(self):
    self.physics.elasticity = 0.4

circle1 = Circle((100,60), 10,color=(255, 100, 255))
circle2 = Circle((100, 65), 10, color=(255, 100, 255))
circle3 = Circle((110, 60), 10, color=(200, 100, 255))
circle4 = Circle((120, 60), 10, color=(155, 100, 255))
circle5 = Circle((130, 65), 10, color=(255, 120, 255))
circle6 = Circle((130, 55), 10, color=(255, 140, 255))
circle7 = Circle((130, 45), 10, color=(255, 180, 255))
circle8 = Circle((130, 30), 10, color=(255, 220, 255))
circle9 = Circle((130, 20), 10, color=(255, 100, 200))

# line 3
line3 = Line((80, 150), (100, 200), 10, color=(100, 50, 100))
@line3.register
def setup_physics(self):
    self.physics.elasticity = 0.1

my_board.run()
