from miniworldmaker import *
import random
board = PhysicsBoard(400, 400)
board.debug = False
board.add_background((255,255,255))
line = Line((10, 40), (200, 300), 1, color=(100, 100, 255))
circles = []
for i in range(2):
    circle = Circle((random.randint(40,100), 20), 20, 0,
                     color=(random.randint(0,255),
                            random.randint(0,255),
                            random.randint(0,255)))
    circles.append(circle)
line2 = Line((0, 200), (398, 400), 2, color=(100, 100, 255))
line2.physics.simulation = "manual"
board.run()
