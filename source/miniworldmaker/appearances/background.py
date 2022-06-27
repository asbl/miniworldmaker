from typing import Union, Tuple

import pygame

import miniworldmaker.appearances.appearance as appearance
import miniworldmaker.appearances.managers.image_background_manager as image_background_manager
import miniworldmaker.appearances.managers.transformations_background_manager as transformations_background_manager
import miniworldmaker.base.app as app


class Background(appearance.Appearance):
    """
    The class describes the background of a board.

    A ``background`` can be an image or a color:

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

    def __init__(self, board=None):
        super().__init__()
        self._fill_color = (150, 150, 150, 255)  # for default image
        self.parent = board  #: The parent of a Background is the associated board.
        # Register image actions which you can be triggered
        self._grid = False
        self._grid_color = (255, 0, 255)
        self.surface = pygame.Surface((self.board.container_width, self.board.container_height))
        self._is_scaled_to_tile = False
        self._image = pygame.Surface((self.parent.width, self.parent.height))  # size set in image()-method
        self.reload_costumes_queue = []
        self.is_scaled = True
        self.transformations_manager = transformations_background_manager.TransformationsBackgroundManager(self)
        self.image_manager = image_background_manager.ImageBackgroundManager(self)

    @property
    def board(self) -> "board.Board":
        return self.parent
    
    def show_grid(self):
        self.grid = True

    @property
    def grid(self) -> Union[bool, tuple]:
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
    def grid(self, value):
        self._grid = value
        self.set_dirty("all", Background.LOAD_NEW_IMAGE)

    def repaint(self):
        """Called 1/frame from board"""
        if self.parent == app.App.board:
            self.board.tokens.clear(self.surface, self.image)
            repaint_rects = self.board.tokens.draw(self.surface)
            self.board.app.window.repaint_areas.extend(repaint_rects)

    def _update_all_costumes(self):
        """updates costumes for all tokens on board"""
        [token.costume.update() for token in self.reload_costumes_queue]
        self.reload_costumes_queue = []
        if hasattr(self.board, "dynamic_tokens"):
            dynamic_tokens = self.board.dynamic_tokens.copy()
            [token.costume.update() for token in dynamic_tokens]
            del(dynamic_tokens)

    def _after_transformation_pipeline(self):
        self.surface = pygame.Surface((self.board.container_width, self.board.container_height))
        self.surface.blit(self.image, self.surface.get_rect())
        for token in self.board.camera.get_tokens_in_viewport():
            token.dirty = 1
        self._blit_to_window_surface()
        self._update_all_costumes()

    def _blit_to_window_surface(self):
        """Blits background to window surface"""
        if self.parent == app.App.board:
            self.parent.app.window.surface.blit(self.image, (0, 0))
            self.parent.app.window.add_display_to_repaint_areas()
            self.repaint()

    def add_image(self, source: Union[str, Tuple, pygame.Surface]) -> int:
        super().add_image(source)
        self._blit_to_window_surface()
        self._update_all_costumes()
        if self.parent == app.App.board:
            self.parent.app.window.surface.blit(self.image, (0, 0))
            self.parent.app.window.add_display_to_repaint_areas()
            return self.parent.app.window.display_update()