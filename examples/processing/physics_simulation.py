from miniworldmaker import *
import random
board = PixelBoard(400, 400)
board.add_background((255,255,255))
line = Line((0, 40), (400, 400), 1, color=(100, 100, 255))
line.physics.friction = 1
line.start_physics()
circles = []
for i in range(100):
    circle = Circle((random.randint(40,100), 20), 20, 0,
                     color=(random.randint(0,255),
                            random.randint(0,255),
                            random.randint(0,255)))
    circle.physics.elasticity = 1
    circle.physics.mass = 10
    circle.start_physics()
    circles.append(circle)
line2 = Line((398, 200), (398, 400), 1, color=(100, 100, 255))
line2.start_physics()
@line2.register
def on_touching_token(self, token, info):
    print("touching")
    if token in circles:
        circle.direction = -10
        circle.impulse_in_direction(1000)
        print("impulse")
board.run()
