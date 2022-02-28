from typing import Union

import pygame
from miniworldmaker.appearances import appearance
from miniworldmaker.appearances.managers import transformations_background_manager


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
        self.board = board
        # Register image actions which you can be triggered
        self._grid_overlay = False
        self._is_scaled_to_tile = False
        self._image = pygame.Surface((self.parent.width, self.parent.height))  # size set in image()-method
        self.is_scaled = True
        self.transformations_manager = transformations_background_manager.TransformationsBackgroundManager(self)

    def add_image(self, path):
        super().add_image(path)
        self.parent.app.window.display_update()

    def next_image(self):
        """Switches to the next image of the appearance.
        """
        super().next_image()
        self.parent.window.repaint_areas.append(self.image.get_rect())
        self.parent.window.window_surface.blit(self.image, (0, 0))

    @property
    def grid_overlay(self) -> Union[bool, tuple] :
        """If not False, a grid overlay is drawn over the background image.

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
            self.reload_transformations_after("grid_overlay")
        else:
            self._grid_overlay = False
            self.reload_transformations_after("grid_overlay")

    @property
    def is_scaled_to_tile(self) -> bool:
        """Scales the image to Tile_size.

        The method is needed if you want to texture the background on a Tiled_Board
        and want the texture to fill one tile at a time.

        Examples:
            Defines a textured board

            >>> class MyBoard(TiledBoard):
            >>>    def on_setup(self):
            >>>         self.add_image(path="images/stone.png")
            >>>         self.background.is_textured = True
            >>>         self.background.is_scaled_to_tile = True
            >>>         self.player = Player(position=(3, 4))
        """
        return self._is_scaled_to_tile

    @is_scaled_to_tile.setter
    def is_scaled_to_tile(self, value):
        self._is_scaled_to_tile = value
        self.reload_transformations_after("scale_to_tile")


