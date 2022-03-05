from typing import Union

import pygame
from miniworldmaker.appearances import appearance
from miniworldmaker.appearances.managers import transformations_background_manager


class Background(appearance.Appearance):
    """
    The class describes the background of a board.

    A ``background`` can be an image or an color:

    Each board has one or more backgrounds that can be switched between.
    In addition, each background also has several pictures (or colors) between which you can switch.

    Examples:

        Add an image as background

        .. code-block:: python

            board = Board()
            Board.add_background(images/my_image.png)
        
        Add a color as background:

        .. code-block:: python

            board = Board()
            Board.add_background((255, 0,0, 0))

        ..or alternative way: Create background with property:

        .. code-block:: python

            from miniworldmaker import *

            board = Board()
            board.background =(255,0,0)
            board.run()

    """

    def __init__(self, board):
        super().__init__()
        self.parent = board  #: The parent of a Background is the associated board.
        self.board = board
        # Register image actions which you can be triggered
        self._grid = False
        self._is_scaled_to_tile = False
        self._image = pygame.Surface((self.parent.width, self.parent.height))  # size set in image()-method
        self.is_scaled = True
        self.transformations_manager = transformations_background_manager.TransformationsBackgroundManager(self)

    def add_image(self, path):
        super().add_image(path)
        self.parent.app.window.display_update()

    def show_grid(self):
        self.grid = True

    @property
    def grid(self) -> Union[bool, tuple] :
        """Shows a grid-overlay

        grid can be `True`, `False` or a color-tuple

        Examples:

            Show grid:

            .. code-block:: python

                from miniworldmaker import *

                board = TiledBoard(4,4)
                board.tile_margin = 10
                background = board.add_background("images/stone.png")
                background.is_textured = True
                token = Token()
                @token.register
                def on_key_down(self, key):
                    self.move_right()
                background.grid = True
                board.run()

            .. image:: ../_images/grid.png
                :alt: Textured image

        """
        return self._grid

    @grid.setter
    def grid(self, color=(255, 255, 255, 255)):
        if color is True:
            self._grid = True
            color = (200, 80, 60)
        if color is not False:
            self._grid = True
            self.color = color
            self.reload_transformations_after("grid")
        else:
            self._grid = False
            self.reload_transformations_after("grid")
        self.parent.view_handler.full_repaint()

