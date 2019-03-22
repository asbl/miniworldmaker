from miniworldmaker import *
import random


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(tile_size=100, columns=3, rows=3, tile_margin=1)
        self.window.add_container(MyToolbar(), dock="right")
        self.arrow = Arrow()
        self.add_to_board(self.arrow, (1, 1))
        self.chip = None
        self.placed = False
        self.add_image("images/greenfield.jpg")

    def get_event(self, event, data):
        print(event, data)
        if event == "button":
            if data == "Spin":
                self.arrow.spin()
        if event == "mouse_left" and self.placed is False:
            position = self.pixel_to_grid_position(data)
            if not position == (1, 1):
                self.chip = Chip()
                self.add_to_board(self.chip, position)
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
                if self.is_looking_at_tokens(direction="forward", actor_type=Chip):
                    self.board.message_box("Du hast gewonnen")
                else:
                    self.board.message_box("Du hast verloren")

    def spin(self):
        self.spinning = random.randint(600, 800)
        self.board.places = False


class Chip(Token):

    def __init__(self):
        super().__init__()
        self.add_image("images/chip.png")


class MyToolbar(Toolbar):

    def __init__(self):
        super().__init__()
        button = ToolbarButton("Spin")
        self.add_widget(button)
        print("size", button.width, button.height)


my_grid = MyBoard()
my_grid.show()
