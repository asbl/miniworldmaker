from tools import appearance
import pygame


class Costume(appearance.Appearance):

    def __init__(self, token):
        self.token = token
        super().__init__()
        self.upscale = True

    def changed(self):
        self.token.dirty = 1

    @property
    def image(self) -> pygame.Surface:
        self._renderer.direction = self.token.direction
        self._renderer.size = self.token.size
        self._renderer.orientation = self.token.orientation
        self._renderer.flipped = self.token._flip_x
        self._image = self._renderer.get_image()
        return self._image
