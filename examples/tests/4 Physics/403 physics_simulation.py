from miniworldmaker import *
import random
board = PhysicsBoard(400, 400)
print(board.token_handler)
board.add_background((255,255,255))
line = Line((20, 200), (300, 220), 2, color=(100, 100, 255))
line.physics.friction = 1
line.physics.simulation = "manual"
circles = []
for i in range(10):
    circle = Circle((random.randint(40,100), 20), 20, 0,
                     color=(random.randint(0,255),
                            random.randint(0,255),
                            random.randint(0,255)))
    circle.physics.elasticity = 1
    circle.physics.mass = 10
    circles.append(circle)
#line2 = Line((398, 200), (398, 400), 2, color=(100, 100, 255))
#line2.physics.simulation = "manual"
board.run()
