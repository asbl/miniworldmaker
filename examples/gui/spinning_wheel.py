from gamegridp import *
import random


class MyGrid(CellGrid, GUIGrid):

    def __init__(self):
        super().__init__(cell_size=100, columns=3, rows=3, margin=1)
        self.window.add_container(MyToolbar(), dock="right")
        self.arrow = Arrow()
        self.add_actor(self.arrow, (1, 1))
        self.chip = None
        self.placed = False
        self.add_image("images/greenfield.jpg")

    def get_event(self, event, data):
        print(event, data)
        if event == "button":
            if data == "Spin":
                self.arrow.spin()
        if event == "mouse_left" and self.placed is False:
            cell = self.pixel_to_cell(data)
            if not cell == (1, 1):
                self.chip = Chip()
                self.add_actor(self.chip, cell)
                self.placed = True
        print(self.actors)


class Arrow(Actor):

    def __init__(self):
        super().__init__()
        self.spinning = 0
        self.add_image("images/arrow.png")

    def act(self):
        if self.spinning > 0:
            self.turn_left((self.spinning/800)*20)
            self.spinning = self.spinning - 1
            if self.spinning == 0:
                if self.grid.get_actors_at_location(self.look(direction = "forward")):
                    self.grid.message_box("Du hast gewonnen")
                else:
                    self.grid.message_box("Du hast verloren")

    def spin(self):
        self.spinning = random.randint(600, 800)
        self.grid.places = False


class Chip(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("images/chip.png")


class MyToolbar(Toolbar):

    def __init__(self):
        super().__init__()
        button = ToolbarButton("Spin")
        self.add_widget(button)
        print("size", button.width, button.height)


my_grid = MyGrid()
my_grid.show()
