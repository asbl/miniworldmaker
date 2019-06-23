import random

from miniworldmaker import *


class MyBoard(ProcessingBoard):

    def on_setup(self):
        self.fill((255, 255, 255, 255))
        self.lst = []
        for i in range(50):
            self.lst.append(Circle((random.randint(0, 800), random.randint(0, 600)), random.randint(10, 20), 0, color=(255, 0, 0, 100)))

    def act(self):
        for circle in self.lst:
            circle.y -= (21 - circle.radius) / 2


my_board = MyBoard(800, 600)
my_board.show()
