from typing import Union

import pygame
from miniworldmaker.tools import appearance


class Background(appearance.Appearance):
    """
    The class describes the background of a board.

    Each board has one or more backgrounds that can be switched between.
    In addition, each background also has several pictures between which you can switch.

    You can scale a background or tile it like a texture.
    """

    def __init__(self, board):
        super().__init__()
        self.parent = board  #: The parent of a Background is the associated board.
        # Register image actions which you can be triggered
        self._grid_overlay = False
        self._is_scaled_to_tile = False
        self.image_actions_pipeline = [("scale_to_tile", self.image_action_scale_to_tile,
                                        "is_scaled_to_tile")] + self.image_actions_pipeline
        self.image_actions_pipeline.append(("grid_overlay", self.image_action_show_grid, "grid_overlay"))
        self.is_scaled = True,
        self.alpha = False

    def next_image(self):
        """
        Switches to the next image of the appearance.
        """
        super().next_sprite()
        self.parent.window.repaint_areas.append(self.image.get_rect())
        self.parent.window.window_surface.blit(self.image, (0, 0))

    @property
    def grid_overlay(self) -> Union[bool, tuple] :
        """
        If not False, a grid overlay is drawn over the background image.

        Examples:
            >>> a_token.background.grid_overlay = (255, 0, 0, 0)
            Draws a red (255, 0, 0, 0) background overlay

            >>> a_token.background.grid_overlay = False
            Disables background grid_overlay

            >>> a_token.background.grid_overlay = ()
            Disables background grid_overlay. Same as a_token.background.grid_overlay = False

        """
        return self._grid_overlay

    @grid_overlay.setter
    def grid_overlay(self, color=(255, 255, 255, 255)):
        if color is True:
            self._grid_overlay = True
            color = (200, 80, 60)
        if color is not False:
            self._grid_overlay = True
            self.color = color
            self.call_action("grid_overlay")
            self.dirty = 1
        else:
            self._grid_overlay = False
            self.call_action("grid_overlay")
            self.dirty = 1
        print("overlay set to", self.color)

    @property
    def is_scaled_to_tile(self) -> bool:
        """Scales the image to Tile_size.

        The method is needed if you want to texture the background on a Tiled_Board
        and want the texture to fill one tile at a time.

        Examples:
            >>> a_tiled_board.background.is_textured = True
            >>> a_tiled_board.is_scaled_to_tile = True
            The image is scaled to tile size and then the background is wallpapered with the image.
        """
        return self._is_scaled_to_tile

    @is_scaled_to_tile.setter
    def is_scaled_to_tile(self, value):
        self._is_scaled_to_tile = value
        self.dirty = 1

    def image_action_show_grid(self, image: pygame.Surface, parent) -> pygame.Surface:
        i = 0
        while i <= parent.width:
            pygame.draw.rect(image, self.color, [i, 0, parent.tile_margin, parent.height])
            i += parent.tile_size + parent.tile_margin
        i = 0
        while i <= parent.height:
            pygame.draw.rect(image, self.color, [0, i, parent.width, parent.tile_margin])
            i += parent.tile_size + parent.tile_margin
        return image

    def image_action_scale_to_tile(self, image: pygame.Surface, parent) -> pygame.Surface:
        image = pygame.transform.scale(image, (self.parent.tile_size, self.parent.tile_size))
        with_margin = pygame.Surface((parent.tile_size + parent.tile_margin, parent.tile_size + parent.tile_margin))
        with_margin.blit(image, (parent.tile_margin, parent.tile_margin))
        return with_margin
