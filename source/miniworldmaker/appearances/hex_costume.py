
import pygame
from typing import List

import sys
from miniworldmaker import conf

sys.path.append(conf.ROOT_DIR)


from boards.elements import hex_elements
from appearances import costume
from tokens import hex_tokens
import miniworldmaker
class HexCostume(costume.Costume):
    def __init__(self, token : "hex_tokens.HexToken"):
        super().__init__(token)
        self.set_image((0, 0, 0, 0))
        self.is_scaled = True
        self.is_upscaled = False
        self.is_filled = True
        self.mod_pointlist = []
        self.fill_color = (180, 180, 180, 255)
        self.border = 1
        self.border_color = (100, 100, 100, 255)
        self._update_draw_shape()

    def _update_draw_shape(self):
        self.mod_pointlist = []
        board = self.token.board
        if board.is_tile(self.token.position):
            tile = self.token.board.get_tile(self.token.position)
            for corner in tile.get_neighbour_corners():
                offset = corner.get_local_coordinate_for_tile(tile)
                if offset:
                    self.mod_pointlist.append(offset)
        else:
            pass
        super()._update_draw_shape()
            
    def _inner_shape(self):
        board = self.token.board
        if board.is_tile(self.token.position):
            return pygame.draw.polygon, [self.mod_pointlist, 0]
        elif board.is_corner(self.token.position):
            return pygame.draw.rect, [pygame.Rect(0,0, self.token.size[0], self.token.size[1]), 0]
        elif board.is_edge(self.token.position):
            return pygame.draw.rect, [pygame.Rect(0,0, self.token.size[0], self.token.size[1]), 0]
        
    def _outer_shape(self):
        board = self.token.board
        if board.is_tile(self.token.position):
            return pygame.draw.polygon, [self.mod_pointlist, self.border]
        elif board.is_corner(self.token.position):
            return pygame.draw.rect, [pygame.Rect(0,0, self.token.size[0], self.token.size[1]), self.border]
        elif board.is_edge(self.token.position):
            return pygame.draw.rect, [pygame.Rect(0,0, self.token.size[0], self.token.size[1]), self.border]
