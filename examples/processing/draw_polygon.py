from miniworldmaker import *


class MyBoard(ProcessingBoard):

    def __init__(self):
        super().__init__()
        self.pointlist = []

    def get_event(self, event, data):
        if event == "mouse_left":
            self.pointlist.append(self.get_mouse_position())
        if event == "mouse_right":
            Polygon(pointlist=self.pointlist, color=(255, 255, 0, 255))
            self.pointlist = []



my_board = MyBoard()
my_board.show()

