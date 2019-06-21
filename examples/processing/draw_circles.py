from miniworldmaker import *


class MyBoard(ProcessingBoard):

    color = (255, 255, 255, 50)

    def act(self):
        Ellipse(self.get_mouse_position(), 80, 80, 1, MyBoard.color)

    def get_event(self, event, data):
        if event == "mouse_left":
            MyBoard.color = (200, 100, 100, 50)
        if event == "mouse_right":
            MyBoard.color = (255, 255, 255, 50)


my_board = MyBoard()
my_board.show()

