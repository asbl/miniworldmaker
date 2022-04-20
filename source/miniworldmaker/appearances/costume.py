import pygame
import miniworldmaker.appearances.appearance as appear
import miniworldmaker.appearances.managers.transformations_costume_manager as transformations_costume_manager


class Costume(appear.Appearance):
    """A costume contains one or multiple images

    Every token has a costume which defines the "look" of the token.
    You can switch the images in a costume to animate the token.

    A costume is created if you add an image to an actor with token.add_image(path_to_image)
    """

    def __init__(self, token):
        super().__init__()
        self._fill_color = (255, 0, 255, 100)
        self._border_color = (100, 100, 100)
        self.parent = token  #: the parent of a costume is the associated token.
        self.board = token.board
        self.token = self.parent
        self._info_overlay = False
        self._is_rotatable = True
        self.transformations_manager = transformations_costume_manager.TransformationsCostumeManager(self)

    def after_init(self):
        super().after_init()
        self.set_default_color_values()
        self._update_shape()

    def set_default_color_values(self):
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
        self.reload_transformations_after(
            "all",
        )

    def _update_shape(self):
        if self.token.position_manager:
            self._update_draw_shape()

    def get_token_rect(self):
        if self.token.dirty == 1:
            self._rect = self._reload_token_rect_from_costume()
            return self._rect
        else:
            return self._rect

    def _reload_dirty_image(self):
        self._update_shape()
        super()._reload_dirty_image()

    def set_image(self, source) -> bool:
        super().set_image(source)

    def _inner_shape(self):
        return pygame.draw.rect, [pygame.Rect(0, 0, self.parent.size[0], self.parent.size[1]), 0]

    def _outer_shape(self):
        return pygame.draw.rect, [pygame.Rect(0, 0, self.parent.size[0], self.parent.size[1]), self.border]

    def _update_draw_shape(self):
        self.draw_shapes = []
        if self._inner_shape():
            if self.is_filled:
                self.draw_shape_append(self._inner_shape()[0], self._inner_shape_arguments())
        if self._outer_shape():
            if self.border:
                self.draw_shape_append(self._outer_shape()[0], self._outer_shape_arguments())

    def _inner_shape_arguments(self):
        if not self.fill_color:
            color = (255, 0, 255)
        else:
            color = self.fill_color
        return [
                   color,
               ] + self._inner_shape()[1]

    def _outer_shape_arguments(self):
        if not self.border_color:
            color = (255, 0, 255)
        else:
            color = self.border_color
        return [
                   color,
               ] + self._outer_shape()[1]
