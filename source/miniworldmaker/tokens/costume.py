from miniworldmaker.tools import appearance
import pygame
from miniworldmaker.tools import image_renderers as ir


class Costume(appearance.Appearance):

    def __init__(self, token):
        super().__init__()
        self.parent = token
        self.is_upscaled = True
        self.is_rotatable = True
        self.register_action("info_overlay", ir.ImageRenderer.info_overlay)

    def update(self):
        if self.parent.board:
            if self.parent.board.frame % self.animation_speed == 0:
                self.next_sprite()

    def set_costume(self, index):
        self._image_index = index

    def show_info_overlay(self, color=(255, 255, 255, 255)):
        """
        Shows info overlay (Rectangle around the token and Direction marker)
        Args:
            color: Color of info_overlay
        """
        self.parent.dirty = 1
        self.color = color
        self.enabled_image_actions["info_overlay"] = True
        self.call_action("info_overlay")

    def hide_info_overlay(self):
        self.parent.dirty = 1
        self.enabled_image_actions["info_overlay"] = False
        self.call_action("info_overlay")