import math

import pygame
from miniworldmaker.appearances import appearance as appear
from miniworldmaker.appearances.managers import transformations_costume_manager

class Costume(appear.Appearance):
    """A costume contains one or multiple images

    Every token has a costume which defines the "look" of the token.
    You can switch the images in a costume to animate the token.

    A costume is created if you add an image to an actor with token.add_image(path_to_image)
    """

    def __init__(self, token):
        super().__init__()
        self.parent = token  #: the parent of a costume is the associated token.
        self.board = token.board
        self.token = self.parent
        self._is_upscaled = True
        self._info_overlay = False
        self._is_rotatable = True
        self.transformations_manager = transformations_costume_manager.TransformationsCostumeManager(self)

    @property
    def info_overlay(self):
        return self._info_overlay

    @info_overlay.setter
    def info_overlay(self, value):
        """
        Shows info overlay (Rectangle around the token and Direction marker)
        Args:
            color: Color of info_overlay
        """
        self._info_overlay = value
        self.dirty = 1
        self._reload_all()