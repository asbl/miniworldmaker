from miniworldmaker import *


class MyBoard(PixelBoard):

    def on_setup(self):
        self.color = (255, 255, 255, 50)
        self.add_background((0,0,0,255))

    def act(self):
        Circle(self.get_mouse_position(), 80, 1, self.color)

    def on_mouse_left(self, mouse_pos):
        self.color = (200, 100, 100, 50)

    def on_mouse_right(self, mouse_pos):
        self.color = (255, 255, 255, 50)


my_board = MyBoard(800, 600)
my_board.run()

