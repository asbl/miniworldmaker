from tools import image_renderer
import pygame


class Appearance:

    def __init__(self):
        self._renderer = image_renderer.ImageRenderer()
        self._image = self._renderer.get_image()
        self.animation_speed = 60
        self.scale_x = True
        self.scale_y = True
        self.set_upscale = False
        self._is_animated = False

    def add_image(self, path: str) -> int:
        return self._renderer.add_image(path)

    @property
    def upscale(self):
        return self._renderer.image_actions["upscale"]

    @upscale.setter
    def upscale(self, value):
        if value == True:
            self._renderer.image_actions["scale_x"] = False
            self._renderer.image_actions["scale_y"] = False
            self._renderer.image_actions["upscale"] = True
        else:
            self._renderer.image_actions["upscale"] = False

    @property
    def scale_x(self):
        return self._renderer.image_actions["scale_x"]

    @scale_x.setter
    def scale_x(self, value):
        self._renderer.image_actions["scale_x"] = value
        self.changed()

    @property
    def scale_y(self):
        return self._renderer.image_actions["scale_y"]

    @scale_y.setter
    def scale_y(self, value):
        self._renderer.image_actions["scale_y"] = value
        self.changed()

    @property
    def is_rotatable(self):
        return self._renderer.image_actions["rotatable"]

    @is_rotatable.setter
    def is_rotatable(self, value):
        self._renderer.image_actions["rotatable"] = value
        self.changed()

    @property
    def overlay(self):
        return self._renderer.image_actions["info_overlay"]

    @overlay.setter
    def overlay(self, value):
        self._renderer.image_actions["info_overlay"] = value
        self.changed()

    @property
    def image(self) -> pygame.Surface:
        pass

    def next_sprite(self):
        self._renderer.next_sprite()

    @property
    def is_animated(self):
        return self._is_animated

    @is_animated.setter
    def is_animated(self, value):
        self._is_animated = value
        self.changed()

    def changed(self):
        pass
