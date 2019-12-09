import random

import easygui
from miniworldmaker import *


class MyBoard(TiledBoard):

    def on_setup(self):
        self.tile_size = 100
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

    def on_mouse_left(self, mouse_pos):
        if not self.placed:
            position = self.get_board_position_from_pixel(mouse_pos)
            print(position)
            if not position == (1, 1):
                self.chip = Chip(position)
                if self.chip:
                    self.placed = True

class Arrow(Actor):

    def on_setup(self):
        self.spinning = 0
        self.add_image("images/arrow.png")

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
        self.add_image("images/chip.png")

my_grid = MyBoard(3, 3)
my_grid.show()
