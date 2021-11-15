from typing import Union
from miniworldmaker.appearances import background

import pymunk as pymunk_engine
from miniworldmaker.board_positions import board_position
from miniworldmaker.boards import pixel_board  as pixel_board_module
import miniworldmaker.tokens.token as token_module
from miniworldmaker.boards.board_handler.board_token_handler import board_physicsboardtokenhandler as physicshandler

class PhysicsBoard(pixel_board_module.PixelBoard):

    def __init__(self,
                 columns: int = 40,
                 rows: int = 40,
                 tile_size : int = 1,
                 tile_margin : int = 0,
                 background_image=None
                 ):
            self.token_handler = physicshandler.PhysicsBoardTokenHandler(self)
            self.gravity_x = 0
            self.gravity_y = -900
            self.debug = False
            self.collision_types = list
            self.accuracy = 1
            self.space = pymunk_engine.Space()
            self.space.gravity = self.gravity_x, self.gravity_y
            self.space.iterations = 35
            self.space.damping = 0.9
            self.space.collision_persistence = 10
            # Note: This is the grandparent constructor
            super(pixel_board_module.PixelBoard, self).__init__(columns, rows, tile_size, tile_margin, background_image)
            
    @property
    def gravity(self):
        return self.gravity_x, self.gravity_y

    @gravity.setter
    def gravity(self, value: tuple):
        self.gravity_x = value[0]
        self.gravity_y = value[1]
        self.space.gravity = self.gravity_x, self.gravity_y

    @property
    def damping(self):
        return self.gravity_x, self.gravity_y

    @damping.setter
    def damping(self, value: tuple):
        self._damping = value
        self.space.damping = self._damping