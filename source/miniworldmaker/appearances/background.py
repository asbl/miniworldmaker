from typing import Union

import pygame
from miniworldmaker.appearances import appearance


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
        self.image_actions_pipeline = [("scale_to_tile", self.image_action_scale_to_tile,
                                        "is_scaled_to_tile")] + self.image_actions_pipeline
        self.image_actions_pipeline.append(("grid_overlay", self.image_action_show_grid, "grid_overlay"))
        self._image = pygame.Surface((self.parent.width, self.parent.height))  # size set in image()-method

    def add_image(self, path):
        super().add_image(path)
        self.parent.app.window.display_update()

    def after_init(self):
        super().after_init()
        self.is_scaled = True

    def next_image(self):
        """
        Switches to the next image of the appearance.
        """
        super().next_image()
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
        self.call_action("scale_to_tile")

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

    async def _update(self):
        if self.is_animated:
            if self.parent.board.frame % self.animation_speed == 0:
                self.next_image()
                self.reload_image()
        else:
            self.reload_image()