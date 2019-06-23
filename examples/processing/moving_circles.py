import random

from miniworldmaker import *


class MyBoard(ProcessingBoard):

    def on_setup(self):
        self.fill((255, 255, 255, 255))
        self.lst = []
        for i in range(50):
            self.lst.append(Circle((random.randint(0, 800),
                                    random.randint(200, 600)),
                                   random.randint(40, 80),
                                   0,
                                   color=(100, 0, 255, 100)))

    def act(self):
        for circle in self.lst:
            circle.y -= (81 - circle.radius) / 10


my_board = MyBoard(800, 600)
my_board.show()
