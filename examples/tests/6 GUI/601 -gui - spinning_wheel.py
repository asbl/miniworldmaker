import random

import easygui
from miniworldmaker import *


class MyBoard(TiledBoard):

    def on_setup(self):
        self.tile_size = 100
        toolbar = self.add_container(Toolbar(), dock="right")
        toolbar.add_widget(ToolbarButton("Spin"))
        self.arrow = Arrow((1, 1))
        self.chip = None
        self.placed = False
        self.speed = 1
        self.add_background("images/greenfield.jpg")

    def on_message(self, message):
        if message == "Spin":
                if self.placed:
                    self.arrow.spin()
                else:
                    easygui.msgbox("Du musst zuerst einen Chip setzen")

    def on_mouse_left(self, mouse_pos):
        if not self.placed:
            position = self.get_board_position_from_pixel(mouse_pos)
            if not position == (1, 1):
                self.chip = Chip(position)
                if self.chip:
                    self.placed = True

class Arrow(Token):

    def on_setup(self):
        self.spinning = 0
        self.add_costume("images/arrow.png")

    def act(self):
        if self.spinning > 0:
            self.turn_left((self.spinning/800)*20)
            self.spinning = self.spinning - 1
            if self.spinning == 0:
                if self.sensing_tokens(token_type=Chip):
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

    def on_setup(self):
        self.add_costume("images/chip.png")

my_grid = MyBoard(3, 3)
my_grid.run()
