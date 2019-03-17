from miniworldmaker import *


class MyGrid(PixelBoard):

    def __init__(self):
        super().__init__(columns=200, rows=240)
        self.window.add_container(MyToolbar(), dock="right")
        self.rocket = self.add_actor(Rocket(), position = (100, 200))
        self.add_image("images/galaxy.jpg")


    def get_event(self, event, data):
        if event == "button":
            if data == "Start Rocket":
                self.rocket.started = True


class Rocket(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("images/ship.png")
        self.started = False
        self.turn_left(90)
        self.orientation = 270

    def act(self):
        if self.started:
            if not self.grid.is_in_grid(self.look(direction="up")):
                self.remove()
            else:
                self.move(distance = 1, direction = "up")


class MyToolbar(Toolbar):

    def __init__(self):
        super().__init__()
        button = ToolbarButton("Start Rocket")
        self.add_widget(button)


my_grid = MyGrid()
my_grid.show()
