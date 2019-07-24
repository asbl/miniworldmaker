from miniworldmaker import *


class MyBoard(ProcessingBoard):

    def __init__(self):
        super().__init__(800, 600)
        self.background.fill_color = (0, 0, 0, 255)
        self.point = 1
        self.start_pos = None
        self.end_pos = None
        Line((30, 30), (80, 80), 1)
        Circle((200, 200), 100, 0)
        Ellipse((500, 100), 50, 50, color=(255, 0, 0, 255), thickness=2)

    def on_mouse_left(self, mouse_position):
        if self.point == 1:
            self.start_pos = self.get_mouse_position()
            self.point = 2
        elif self.point == 2:
            self.end_pos = self.get_mouse_position()
            print(self.start_pos)
            Line(self.start_pos, self.end_pos, color=(255, 255, 0, 255))
            Point(self.start_pos, color=(255, 0, 0, 255))
            Point(self.end_pos, color=(255, 0, 0, 255), thickness=2)
            print("draw line from {0} to {1}".format(self.start_pos, self.end_pos))
            self.point = 1


my_board = MyBoard()
my_board.show()
