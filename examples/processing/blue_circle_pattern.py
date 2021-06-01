import random

from miniworldmaker import *


class MyBoard(PixelBoard):

    def on_setup(self):
        self.add_background((255, 255, 255, 255))
        i, j = 0, 0
        distance = 30
        while i < self.width/10:
            i += 1
            x = distance * i
            y = i * distance
            self.fill_color = (random.randint(0, 255), random.randint(0, 255), 255, 5 * i)
            Ellipse(position=(x, y), width=i * 10, height=i * 10, thickness=0, color=self.fill_color, )
            j = 0
            while j < self.width/10:
                j += 1
                self.fill_color = (random.randint(0, 255), random.randint(0, 255), 255, 5 * i)
                x, y = (distance * i) - (i * i * j), i * distance
                Ellipse((x, y), i * 10, i * 10, color = self.fill_color, thickness=0)
                x, y = i * distance, (distance * i) - (i * i * j)
                Ellipse((x, y), i * 10, i * 10, color = self.fill_color, thickness=0)



my_board = MyBoard(400, 400)
my_board.run()
