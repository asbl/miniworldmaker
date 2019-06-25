import random

import easygui
from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(tile_size=100, columns=3, rows=3, tile_margin=1)
        toolbar = self.window.add_container(Toolbar(), dock="right")
        toolbar.add_widget(ToolbarButton("Spin"))
        self.arrow = Arrow((1, 1))
        self.chip = None
        self.placed = False
        self.speed = 1
        self.add_image("images/greenfield.jpg")

    def get_event(self, event, data):
        if event == "button":
            if data == "Spin":
                if self.placed:
                    self.arrow.spin()
                else:
                    easygui.msgbox("Du musst zuerst einen Chip setzen")
        if event == "mouse_left" and self.placed is False:
            position = self.get_board_position_from_pixel(data)
            if not position == (1, 1):
                self.chip = Chip(position)
                if self.chip:
                    self.placed = True

class Arrow(Actor):

    def __init__(self, position):
        super().__init__(position)
        self.spinning = 0
        self.add_image("images/arrow.png")

    def act(self):
        if self.spinning > 0:
            self.turn_left((self.spinning/800)*20)
            self.spinning = self.spinning - 1
            if self.spinning == 0:
                if self.sensing_tokens(token=Chip):
                    easygui.msgbox("Du hast gewonnen", "Spinning Wheel")
                    self.board.chip.remove()
                    self.board.placed = False
                else:
                    easygui.msgbox("Du hast verloren", "Spinning Wheel")
                    self.board.chip.remove()
                    self.board.placed = False

    def spin(self):
        self.spinning = random.randint(200, 400)


class Chip(Token):

    def __init__(self, position):
        super().__init__(position)
        self.add_image("images/chip.png")

my_grid = MyBoard()
my_grid.show()
