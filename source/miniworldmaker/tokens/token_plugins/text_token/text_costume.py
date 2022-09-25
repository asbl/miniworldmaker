import pygame

import miniworldmaker.appearances.costume as costume


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
        if not self.token.board.tokens_fixed_size:  # fixed size e.g. on TiledBoards
            self.token.position_manager.set_size((self.get_text_width(), self.font_size))
        if self.token.board.tokens_fixed_size:
            _font_size = 0
            self.font_manager.set_font_size(_font_size, update=False)
            while self.font_manager.get_text_width() < self.token.size[0] and self.font_size < self.token.size[1]:
                _font_size += 1
                self.font_manager.set_font_size(_font_size, update=False)
