from miniworldmaker.appearances import costume
import pygame
import math


class HexCostume(costume.Costume):
    def __init__(self, token):
        super().__init__(token)
        self.set_image((0, 0, 0, 0))
        self.is_scaled = True
        self.is_upscaled = False
        self.is_filled = True
        self.fill_color = (255, 255, 255, 50)
        self.border = 1
        self.border_color = (100, 100, 100, 255)


class HexBorderCostume(HexCostume):
    def __init__(self, token, border_direction):
        self.border_direction = border_direction
        super().__init__(token)

    def get_inner_shapes(self):
        board = self.token.board
        size = board.tile_size
        width = board.get_tile_width()
        height = board.get_tile_height()
        return {
            "no": (pygame.draw.line, [(0, size * 1 / 4), (size / 2, 0), 0]),
            "nw": (pygame.draw.line,[(size / 2, 0), (size, size * 1 / 4), 0]),
            "w": (pygame.draw.line, [(size, size * 1 / 4), (size, size * 3/4), 0]),
            "sw": (pygame.draw.line,[(size / 2, size ), (size, size * 3 / 4), 0]),
            "so": (pygame.draw.line,[(width / 2, height ), (0, height * 3 / 4), 0]),
            "o": (pygame.draw.line,[(0, height * 1/4 ), (0, height * 3 / 4), 0]),
            "no": (pygame.draw.line,[(width / 2, 0 ), (0, height * 1 / 4), 0]),
        }

    def get_outer_shapes(self):
        board = self.token.board
        size = board.tile_size
        width = board.get_tile_width()
        height = board.get_tile_height()
        return {
            "no": (pygame.draw.line, [(0, height * 1 / 4), (width / 2, 0), self.token.border]),
            "nw": (pygame.draw.line,[(width / 2, 0), (width, height * 1 / 4), self.token.border]),
            "w":  (pygame.draw.line,[(width, size * 1/4 ), (width, size * 3 / 4), self.token.border]),
            "sw": (pygame.draw.line,[(width / 2, height ), (width, height * 3 / 4), self.token.border]),
            "so": (pygame.draw.line,[(width / 2, height ), (0, height * 3 / 4), self.token.border]),
            "o": (pygame.draw.line,[(0, height * 1/4 ), (0, height * 3 / 4), self.token.border]),
            "no": (pygame.draw.line,[(width / 2, 0 ), (0, height * 1 / 4), self.token.border]),
        }

    def _inner_shape(self):
        return self.get_inner_shapes()[self.border_direction]

    def _outer_shape(self):
        return self.get_outer_shapes()[self.border_direction]
