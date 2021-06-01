import math

import pygame
from miniworldmaker.appearances import appearance as appear


class Costume(appear.Appearance):
    """ A costume contains one or multiple images

    Every token has a costume which defines the "look" of the token.
    You can switch the images in a costume to animate the token.

    A costume is created if you add an image to an actor with token.add_image(path_to_image)
    """

    def __init__(self, token):
        super().__init__()
        self.parent = token  #: the parent of a costume is the associated token.
        self.costume_id = self.parent.costume_count
        self.parent.costume_count += 1
        self._is_upscaled = True
        self._info_overlay = False
        self._is_rotatable = True
        self.return_to_costume = -1
        self.image_actions_pipeline.append(("info_overlay", self.image_action_info_overlay, "info_overlay"))

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
        self.call_action("info_overlay")

    def set_costume(self, index):
        self._image_index = index

    def image_action_info_overlay(self, image: pygame.Surface, parent) -> pygame.Surface:
        pygame.draw.rect(image, (255, 0, 0, 100),
                         image.get_rect(), 4)
        # draw direction marker on image
        rect = parent.rect
        center = rect.centerx - parent.x, rect.centery - parent.y
        x = center[0] + math.sin(math.radians(parent.direction)) * rect.width / 2
        y = center[1] - math.cos(math.radians(parent.direction)) * rect.width / 2
        start_pos, end_pos = (center[0], center[1]), (x, y)
        pygame.draw.line(image, (255, 0, 0, 100), start_pos, end_pos, 3)
        return image

    def update(self):
        super().update()
        if self.return_to_costume >= 0:
           if self.costume_id != self.return_to_costume:
                    self.parent.switch_costume(self.return_to_costume)

    async def _update(self):
        if self.parent.board and self.is_animated:
            if self._end_animation or (
                    self.parent.board.frame != 0 and self.parent.board.frame % self.animation_speed == 0):
                await self.next_image()
                if self.animation_length > 0:
                    self.animation_length -= 1
                    self.remove_last_image()
                    if self.animation_length == 0:
                        self.current_animation_images = None
                        self.parent.current_animation = None
                        self.current_animation = None
            else:
                self.reload_image()
        else:
            self.reload_image()

    def reset(self):
        self._image_index = 0
        self.end_animation()

    def __str__(self):
        return "Costume for with ID [" + str(self.costume_id) + "] for parent:[" + str(self.parent) + "]"
