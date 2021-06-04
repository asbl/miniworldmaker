from miniworldmaker import *
import random
board = PixelBoard(400, 400)
board.add_background((255,255,255))
line = Line((0, 40), (400, 400), 1, color=(100, 100, 255))
line.start_physics()
for i in range(300):
    circle = Circle((random.randint(40,100), 20), 20, 0,
                     color=(random.randint(0,255),
                            random.randint(0,255),
                            random.randint(0,255)))
    circle.start_physics()
board.run()
