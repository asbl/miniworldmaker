import miniworldmaker.appearances.costume as costume
import pygame
import math

class TextCostume(costume.Costume):
    def __init__(self, token):
        super().__init__(token)
        self.set_image((0, 0, 0, 0))

    def _set_token_default_values(self):
        self.fill_color = (255, 255, 255, 255)
        self.border = 0
        self.is_rotatable = True
        self.border_color = (100, 100, 100, 255)
        self.border = 0

    def _inner_shape(self):
        return None

    def _outer_shape(self):
        return pygame.draw.rect, [pygame.Rect(0, 0, self.parent.size[0], self.parent.size[1]), self.border]

    def _update_draw_shape(self):
        super()._update_draw_shape()
        """Sets self.size by costume.font_size"""
        if not self.token.board.tokens_fixed_size or (
                hasattr(self.token, "fixed_size") and self.token.fixed_size):  # fixed size e.g. on TiledBoards
            if self.token.max_width != 0:
                width = min(self.get_text_width(), self.token.max_width)
            else:
                width = self.get_text_width()
            height = self.get_text_height()
            self.token.set_size((width, height))
        if self.token.board.tokens_fixed_size:
            self.scale_to_size()

    def scale_to_size(self, width=None, height=None):
        if not width:
            width = self.token.size[0]
        if width == 0:
            width = math.inf
        if not height:
            height = self.token.size[1]
        if height == 0:
            height = math.inf
        _font_size = 0
        self.font_manager.set_font_size(_font_size, update=False)
        while self.get_text_width() < width and self.get_text_height() < height:
            _font_size += 1
            self.font_manager.set_font_size(_font_size, update=False)
        return _font_size
