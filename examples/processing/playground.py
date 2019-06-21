from miniworldmaker import *


class MyBoard(ProcessingBoard):

    def on_setup(self):
        self.fill((255, 255, 255, 255))
        self.circle1 = Circle((40, 40), 60, 0, color = (255, 0, 0, 100))
        self.circle2 = Circle((80, 100), 60, 0, color = (0, 255, 0, 100))
        self.circle3 = Circle((120, 40), 60, 0, color = (0, 0, 255, 100))



my_board = MyBoard(230, 200)
my_board.show()
