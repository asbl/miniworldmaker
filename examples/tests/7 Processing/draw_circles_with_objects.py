import miniworldmaker

my_board = miniworldmaker.PixelBoard(800, 600)
my_board.color = (255, 255, 255, 50)
my_board.add_background((0,0,0,255))

@my_board.register
def act(self):
    miniworldmaker.Circle.from_center(self.get_mouse_position(), 80, 1, self.color)

@my_board.register
def on_mouse_left(self, mouse_pos):
    self.color = (200, 100, 100, 50)

@my_board.register
def on_mouse_right(self, mouse_pos):
    self.color = (255, 255, 255, 50)

my_board.run()
