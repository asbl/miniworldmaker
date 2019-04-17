from miniworldmaker.tools import appearance
import pygame


class Costume(appearance.Appearance):

    def __init__(self, token):
        super().__init__()
        self.parent = token
        self.size = self.parent.size
        self.is_upscaled = True
        self.is_rotatable = True
        self.image_actions.append("info_overlay")
        self.enabled_image_actions["info_overlay"] =  False
        self.image_handlers["info_overlay"] = self.info_overlay

    def update(self):
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


    def info_overlay(self, image):
        pygame.draw.rect(image, self.color,
                         (0, 0, image.get_rect().width, image.get_rect().height), 10)
        # draw direction marker on image
        rect = image.get_rect()
        center = rect.center
        x = rect.right
        y = rect.centery
        pygame.draw.line(image, self.color, (center[0], center[1]), (x, y))
        return image