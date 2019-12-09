from miniworldmaker import *


class MyGrid(PixelBoard):

    def __init__(self):
        super().__init__(columns=200, rows=240)
        self.window.add_container(MyToolbar(), dock="right")
        self.rocket = Rocket(position=(100, 200))
        self.add_image("images/galaxy.jpg")


    def get_event(self, event, data):
        if event == "button":
            if data == "Start Rocket":
                self.rocket.started = True


class Rocket(Actor):

    def __init__(self, position):
        super().__init__(position)
        self.add_image("images/ship.png")
        self.started = False
        self.turn_left(90)
        self.direction = "up"

    def act(self):
        if self.started:
            self.move()

    def on_sensing_not_on_board(self):
        self.remove()



class MyToolbar(Toolbar):

    def __init__(self):
        super().__init__()
        button = ToolbarButton("Start Rocket")
        self.add_widget(button)


my_grid = MyGrid()
my_grid.show()
