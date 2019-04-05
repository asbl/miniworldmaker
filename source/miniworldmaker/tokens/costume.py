from tools import appearance
import pygame


class Costume(appearance.Appearance):

    def __init__(self, token):
        self.token = token
        super().__init__()
        self.size = self.token.size
        self.is_upscaled = True
        self.is_rotatable = True

    def update(self):
        if self.token.board.frame % self.animation_speed == 0:
            self.next_sprite()

    def set_costume(self, index):
        self._image_index = index
