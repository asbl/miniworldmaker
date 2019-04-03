from tools import appearance
import pygame


class Costume(appearance.Appearance):

    def __init__(self, token):
        self.token = token
        super().__init__()
        self.upscale = True
        self.changed = set()

    def changed(self):
        self.token.dirty = 1

    def update(self):
        if self.token.board.frame % self.animation_speed == 0:
            self.next_sprite()

    @property
    def image(self) -> pygame.Surface:
        if "direction" in self.changed:
            self._renderer.direction = self.token.direction

        if "size" in self.changed:
            self._renderer.size = self.token.size
        if "flipped" in self.changed:
            self._renderer.flipped = self.token.is_flipped
        if "orientation" in self.changed:
            self._renderer.orientation = self.token.orientation
        self.changed = set()
        self._image = self._renderer.get_image()
        return self._image
