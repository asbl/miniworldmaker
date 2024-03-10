from typing import Union, Tuple

import miniworldmaker.appearances.appearance as appearance
import miniworldmaker.appearances.managers.image_background_manager as image_background_manager
import miniworldmaker.appearances.managers.transformations_background_manager as transformations_background_manager
import miniworldmaker.base.app as app
import pygame
import miniworldmaker.boards.board_templates.pixel_board.board as board_mod


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

    def set_dirty(self, value="all", status=1):
        super().set_dirty(value, status)
        self._blit_to_window_surface()
        if self.board and self.board.is_display_initialized:
            for token in self.board.tokens:
                token.is_display_initialized = True
                if token.costume:
                    token.costume.set_dirty("all", self.LOAD_NEW_IMAGE)

    @property
    def board(self) -> "board_mod.Board":
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
        if self.board in app.App.running_boards:
            self.board.tokens.clear(self.surface, self.image)
            repaint_rects = self.board.tokens.draw(self.surface)
            if self.board.container_top_left_x != 0 or self.board.container_top_left_y != 0:
                new_repaint_rects = []
                for rect in repaint_rects:
                    rect.topleft = self.board.container_top_left_x + rect.topleft[0], self.board.container_top_left_y + rect.topleft[1]
                    new_repaint_rects.append(rect)
                repaint_rects = new_repaint_rects
            self.board.app.window.repaint_areas.extend(repaint_rects)

    def _update_all_costumes(self):
        """updates costumes for all tokens on board"""
        [token.costume.update() for token in self.reload_costumes_queue if token.costume]
        self.reload_costumes_queue = []
        if hasattr(self.board, "dynamic_tokens"):
            [token.costume.update() for token in self.board.dynamic_tokens if token.costume]

    def _after_transformation_pipeline(self) -> None:
        self.surface = pygame.Surface((self.board.container_width, self.board.container_height))
        self.surface.blit(self.image, self.surface.get_rect())
        self._blit_to_window_surface()
        for token in self.board.camera.get_tokens_in_viewport():
            token.dirty = 1

    def _blit_to_window_surface(self):
        """Blits background to window surface"""
        if self.board in app.App.running_boards:
            self.board.app.window.surface.blit(self.image, (
                self.board.container_top_left_x,
                self.board.container_top_left_y))  # @DEBUG: Position changed from (0, 0)
            self.board.app.window.add_display_to_repaint_areas()
            self.repaint()

    def add_image(self, source: Union[str, Tuple, pygame.Surface]) -> int:
        super().add_image(source)
        self._blit_to_window_surface()
        # if self.board in app.App.running_boards:
        #    self.board.app.window.surface.blit(self.image, (
        #        self.board.container_top_left_x,
        #        self.board.container_top_left_y))  # @DEBUG: Position changed from (0, 0)
        #    self.board.app.window.add_display_to_repaint_areas()
        #    return self.board.app.window.display_update()

    def _inner_shape(self) -> tuple:
        """Returns inner shape of costume

        Returns:
            pygame.Rect: Inner shape (Rectangle with size of token)
        """
        size = (self.parent.container_width, self.parent.container_height)
        return pygame.draw.rect, [
            pygame.Rect(0, 0, size[0], size[1]), 0]

    def _outer_shape(self) -> tuple:
        """Returns outer shape of costume

        Returns:
            pygame.Rect: Outer shape (Rectangle with size of tokens without filling.)
        """
        size = (self.parent.container_width, self.parent.container_height)
        return pygame.draw.rect, [
            pygame.Rect(0, 0, size[0], size[1]), self.border]
