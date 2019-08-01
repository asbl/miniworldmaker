from miniworldmaker import *


class MyBoard(ProcessingBoard):

    def on_setup(self):
        self.fill((0, 0, 0, 255))
        self.line1 = Line((0, 100), (600, 800), 5)
        self.line2 = Line((50, 400), (300, 400),5)
        self.circle1 = Circle((70, 20), 5, 0)
        self.line3 = Line((0, 350), (600, 400), 10)
        self.box = Rectangle((300, 90), 80, 80, 0)
        self.box.image.fill((90, 255, 0, 220))

my_board = MyBoard(800, 600)
my_board.show()