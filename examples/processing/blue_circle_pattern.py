import random

from miniworldmaker import *


class MyBoard(ProcessingBoard):

    def on_setup(self):
        self.background.fill((255, 255, 255, 255))
        i, j = 0, 0
        distance = 30
        while i < self.width/10:
            i += 1
            x = distance * i
            y = i * distance
            self.fill_color = (random.randint(0, 255), random.randint(0, 255), 255, 5 * i)
            Ellipse((x, y), i * 10, i * 10, color = self.fill_color, thickness=0)
            j = 0
            while j < self.width/10:
                j += 1
                self.fill_color = (random.randint(0, 255), random.randint(0, 255), 255, 5 * i)
                x, y = (distance * i) - (i * i * j), i * distance
                Ellipse((x, y), i * 10, i * 10, color = self.fill_color, thickness=0)
                x, y = i * distance, (distance * i) - (i * i * j)
                Ellipse((x, y), i * 10, i * 10, color = self.fill_color, thickness=0)



my_board = MyBoard(400, 400)
my_board.show()

