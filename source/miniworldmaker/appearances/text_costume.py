from miniworldmaker.appearances import costume
import pygame

class TextCostume(costume.Costume):
    def __init__(self, token):
        super().__init__(token)
        self.set_image((0, 0, 0, 0))
        self.fill_color = (255, 255, 255, 255)

    def _inner_shape(self):
        return None

    def _outer_shape(self):
        return pygame.draw.rect, [pygame.Rect(0, 0, self.parent.size[0], self.parent.size[1]), self.border]