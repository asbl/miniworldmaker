from miniworldmaker import *


class MyBoard(ProcessingBoard):

    def __init__(self):
        super().__init__()
        self.point = 1
        self.start_pos = None
        self.end_pos = None
        Line((30, 30), (80, 80), 1)

    def get_event(self, event, data):
        if event == "mouse_left":
            if self.point == 1:
                self.start_pos = self.get_mouse_position()
                self.point = 2

            elif self.point == 2:
                self.end_pos = self.get_mouse_position()
                Line(self.start_pos, self.end_pos, color=(255, 255, 0, 255))
                Point(self.start_pos, color=(255,0,0,255))
                Point(self.end_pos, color=(255,0,0,255), thickness=2)
                print("draw line from {0} to {1}".format(self.start_pos, self.end_pos))
                self.point = 1



my_board = MyBoard()
my_board.show()

