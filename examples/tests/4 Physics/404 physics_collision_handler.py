from miniworldmaker import *
import random
board = PhysicsBoard(400, 400)
board.debug = False
board.add_background((255,255,255))
line = Line((10, 40), (200, 300), 1, color=(100, 100, 255))
# y + 28
circles = []
for i in range(10):
    circle = Circle((random.randint(40,100), 20), 20, 0,
                     color=(random.randint(0,255),
                            random.randint(0,255),
                            random.randint(0,255)))
    circles.append(circle)
    @circle.register
    def on_touching_line(self, other, info):
        print("Ouch!")
    @circle.register
    def on_separation_from_line(self, other, info):
        print("Yeah!")
        
line2 = Line((0, 200), (398, 400), 2, color=(100, 100, 255))
line2.physics.simulation = "manual"
board.run()

