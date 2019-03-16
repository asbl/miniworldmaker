from gamegridp import *

class MyGrid(PixelGrid):
    """My Grid with custom setup method."""
    def __init__(self):
        super().__init__(cell_size=1, columns=500, rows=75, margin=0)
        self.add_image("images/water.png")
        player1 = Robot()
        self.add_actor(player1, position=(0, 0))


class Robot(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("images/robot_blue1.png")
        self.add_image("images/robot_blue2.png")
        self.size = (75,75)
        self.animation_speed = 30
        self.animate()

    def act(self):
        if self.grid.is_in_grid(self.look(direction = "forward")):
            self.move(direction = "forward")
        else:
            self.flip_x()


my_grid = MyGrid()
my_grid.show_log()
my_grid.speed = 50
my_grid.show()
