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

    def show_info_overlay(self, color=(255, 255, 255, 255)):
        self.dirty = 1
        self.color = color
        self.enabled_image_actions["info_overlay"] = True
        self.call_action("info_overlay")
