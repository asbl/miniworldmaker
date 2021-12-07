import miniworldmaker


class MyGrid(miniworldmaker.PixelBoard):

    def __init__(self):
        super().__init__(columns=200, rows=240)
        self.add_container(MyToolbar(), dock="right")
        self.rocket = Rocket(position=(100, 200))
        self.add_background("images/galaxy.jpg")

    def on_message(self, message):
        if message == "Start Rocket":
            self.rocket.started = True


class Rocket(miniworldmaker.Token):

    def __init__(self, position):
        super().__init__(position)
        self.add_costume("images/ship.png")
        self.started = False
        self.turn_left(90)
        self.direction = "up"

    def act(self):
        if self.started:
            self.move()

    def on_sensing_not_on_board(self):
        self.remove()


class MyToolbar(miniworldmaker.Toolbar):

    def __init__(self):
        super().__init__()
        button = miniworldmaker.ToolbarButton("Start Rocket")
        self.add_widget(button)


my_grid = MyGrid()
my_grid.run()
