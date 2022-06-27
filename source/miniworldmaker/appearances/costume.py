import pygame
from typing import List, Tuple
import miniworldmaker.appearances.appearance as appear
import miniworldmaker.appearances.managers.transformations_costume_manager as transformations_costume_manager
from miniworldmaker.boards import board

class Costume(appear.Appearance):
    """A costume contains one or multiple images

    Every token has a costume which defines the "look" of the token.
    You can switch the images in a costume to animate the token.

    A costume is created if you add an image to an actor with token.add_image(path_to_image)
    """

    def __init__(self, token):
        super().__init__()
        self.parent = token  #: the parent of a costume is the associated token.
        self.token = self.parent
        self.info_overlay = False
        self.is_rotatable = False
        self.fill_color = None
        self.border_color = None
        self.transformations_manager = transformations_costume_manager.TransformationsCostumeManager(self)

    @property
    def board(self) -> "board.Board":
        return self.parent.board
    
    def after_init(self):
        # Called in metaclass
        self._set_default_color_values()
        super().after_init()

        
    def _set_default_color_values(self):
        self._set_token_default_values()
        self._set_board_default_values()
        
    def _set_token_default_values(self):
        self._info_overlay = False
        self._is_rotatable = True
        self.fill_color = (255, 0, 255, 100)
        self.border_color = (100, 100, 100)
        
    def _set_board_default_values(self):
        if self.token.board.default_fill_color:
            self.fill_color = self.board.default_fill_color
        if self.token.board.default_is_filled:
            self.is_filled = self.board.default_is_filled
        if self.token.board.default_stroke_color:
            self.border_color = self.board.default_stroke_color
        if self.token.board.default_border_color:
            self.border_color = self.board.default_border_color
        if self.token.board.default_border:
            self.border = self.token.board.default_border

    @property
    def info_overlay(self):
        """Shows info overlay (Rectangle around the token and Direction marker)
        Args:
            color: Color of info_overlay
        """
        return self._info_overlay

    @info_overlay.setter
    def info_overlay(self, value):
        self._info_overlay = value
        self.set_dirty("all",Costume.RELOAD_ACTUAL_IMAGE
        )
        
    def set_dirty(self, value, status):
        if value != None and self.parent and self.images:
            self._update_draw_shape()
        super().set_dirty(value, status)


    def set_image(self, source) -> bool:
        super().set_image(source)

    def _inner_shape(self) -> pygame.Rect:
        """Returns inner shape of costume

        Returns:
            pygame.Rect: Inner shape (Rectangle with size of token)
        """
        return pygame.draw.rect, [pygame.Rect(0, 0, self.parent.position_manager.size[0], self.parent.position_manager.size[1]), 0]

    def _outer_shape(self) -> pygame.Rect:
        """Returns outer shape of costume

        Returns:
            pygame.Rect: Outer shape (Rectangle with size of tokens without filling.)
        """
        return pygame.draw.rect, [pygame.Rect(0, 0, self.parent.position_manager.size[0], self.parent.position_manager.size[1]), self.border]

    def _update_draw_shape(self):
        self.draw_shapes = []
        if self._inner_shape() and self.image_manager:
            if self.is_filled and not self.image_manager.is_image():
                self.draw_shape_append(self._inner_shape()[0], self._inner_shape_arguments())
        if self._outer_shape() and self.border:
            self.draw_shape_append(self._outer_shape()[0], self._outer_shape_arguments())

    def _inner_shape_arguments(self) -> List:
        """def setGets arguments for inner shape

        Returns:
            List[]: List of arguments
        """
        
        color = self.fill_color
        return [
            color,
        ] + self._inner_shape()[1]

    def _outer_shape_arguments(self) -> List:
        """Gets arguments for outer shape

        Returns:
            List[]: List of arguments
        """
        color = self.border_color
        return [
            color,
        ] + self._outer_shape()[1]

    def rotated(self):
        if self.board.camera.is_token_in_viewport(self.token):
            self.set_dirty("rotate", self.RELOAD_ACTUAL_IMAGE)

    def resized(self):
        self.set_dirty("scale", self.RELOAD_ACTUAL_IMAGE)

    def visible(self):
        if self.board.camera.is_token_in_viewport(self.token):
            self.set_dirty("all", self.RELOAD_ACTUAL_IMAGE)