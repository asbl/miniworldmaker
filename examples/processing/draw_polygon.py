from miniworldmaker import *


class MyBoard(ProcessingBoard):

    def on_setup(self):
        self.add_background((255,0,255,0))
        self.pointlist = []

    def on_mouse_left(self, pos):
        self.pointlist.append(self.get_mouse_position())

    def on_mouse_right(self, pos):
        Polygon(pointlist=self.pointlist, color=(255, 255, 0, 255))
        self.pointlist = []



my_board = MyBoard(800, 600)
my_board.run()

