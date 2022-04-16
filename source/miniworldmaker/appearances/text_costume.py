import pygame

import sys
from miniworldmaker import conf

sys.path.append(conf.ROOT_DIR)

from appearances import costume


class TextCostume(costume.Costume):
    def __init__(self, token):
        super().__init__(token)
        self.set_image((0, 0, 0, 0))
        self.fill_color = (255, 255, 255, 255)

    def _inner_shape(self):
        return None

    def _outer_shape(self):
        return pygame.draw.rect, [pygame.Rect(0, 0, self.parent.size[0], self.parent.size[1]), self.border]


    def _update_draw_shape(self):
        super()._update_draw_shape()
        """Sets self.size by costume.font_size"""
        if not self.token.board.fixed_size:
            self.token.set_size((self.get_text_width(), self.font_size))
        if self.board.fixed_size:
            self.font_size = 0
            while self.get_text_width() < self.token.size[0] and self.font_size < self.token.size[1]:
                self.font_size += 1
