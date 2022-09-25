import pygame

from miniworldmaker.appearances import background
from miniworldmaker.tokens import token as token_mod


class BoardCameraManager(pygame.sprite.Sprite):

    def __init__(self, view_x, view_y, board):
        super().__init__()
        self.board = board
        self._topleft = (0, 0)
        self._boundary_x = view_x
        self._boundary_y = view_y
        self.viewport = view_x, view_y
        self._tokens_in_last_frame: pygame.sprite.Group = pygame.sprite.Group()
        self._cached_tokens: tuple = (-1, pygame.sprite.Group())

    @property
    def viewport_width(self):
        return self.get_viewport_width()

    @viewport_width.setter
    def viewport_width(self, value):
        if value > self.boundary_x:
            self._boundary_x = value
        self.viewport = (value, self.viewport[1])
        self.reload_camera()

    @property
    def viewport_height(self):
        return self.get_viewport_height()

    @viewport_height.setter
    def viewport_height(self, value):
        if value > self.boundary_y:
            self._boundary_y = value
        self.viewport = (self.viewport[0], value)
        self.reload_camera()

    def get_viewport_width(self):
        return self.viewport[0]

    def get_viewport_height(self):
        return self.viewport[1]

    def get_viewport_width_in_pixels(self):
        """overwritten in TiledCameraManager
        """
        return self.viewport[0]

    def get_viewport_height_in_pixels(self):
        return self.viewport[1]

    @property
    def boundary_x(self):
        return self._boundary_x

    @boundary_x.setter
    def boundary_x(self, value):
        if value < self.viewport_width:
            self.viewport_width = value
        self._boundary_x = value
        self.reload_camera()

    @property
    def boundary_y(self):
        return self._boundary_y

    @boundary_y.setter
    def boundary_y(self, value):
        if value < self.viewport_height:
            self.viewport_height = value
        self._boundary_y = value
        self.reload_camera()

    def reload_camera(self):
        self.clear_camera_cache()
        self.board.app.window.resize()
        self.board.background.set_dirty("all", background.Background.RELOAD_ACTUAL_IMAGE)

    def clear_camera_cache(self):
        self._cached_tokens = (-1, pygame.sprite.Group())

    def get_local_position(self, pos):
        return pos[0] - self.topleft[0], pos[1] - self.topleft[1]

    @property
    def x(self):
        return self.topleft[0]

    @x.setter
    def x(self, value):
        self.topleft = value, self._topleft[1]
        self.reload_tokens_in_viewport()

    @property
    def y(self):
        return self.topleft[1]

    @y.setter
    def y(self, value):
        self.topleft = self._topleft[0], value
        self.reload_tokens_in_viewport()

    @property
    def topleft(self):
        return self._topleft

    @topleft.setter
    def topleft(self, value):
        old_topleft = self._topleft
        self._topleft = value
        if old_topleft != self._topleft:
            self.reload_tokens_in_viewport()

    @property
    def rect(self):
        return self.get_rect()

    def get_rect(self):
        return pygame.Rect(self.topleft[0], self.topleft[1], self.get_viewport_width_in_pixels(),
                           self.get_viewport_height_in_pixels())

    def reload_tokens_in_viewport(self):
        tokens_in_viewport = self.get_tokens_in_viewport()
        for token in tokens_in_viewport:
            token.dirty = 1
        del tokens_in_viewport
    """
    def get_tokens_in_viewport(self) -> pygame.sprite.Group:
        if self._cached_tokens and self.board.frame == self._cached_tokens[0]: # tokens are cached for actual frame.
            tokens_in_frame_and_last_frame = self._cached_tokens[1]
        else:
            sprite = pygame.sprite.Sprite()
            sprite.rect = self.rect
            found_tokens = pygame.sprite.spritecollide(sprite, self.board.tokens, dokill=False)
            self._tokens_in_last_frame = self._cached_tokens[1]
            tokens_in_frame_and_last_frame = pygame.sprite.Group(found_tokens)
            tokens_in_frame_and_last_frame.add(self._tokens_in_last_frame)
            self._cached_tokens = (self.board.frame, tokens_in_frame_and_last_frame)
        return tokens_in_frame_and_last_frame

    """
    def get_tokens_in_viewport(self) -> pygame.sprite.Group:
        if self._cached_tokens and self.board.frame == self._cached_tokens[0]:
            found_tokens = self._cached_tokens[1]
        else:
            found_tokens = pygame.sprite.Group()
            for token in self.board.tokens:
                # token.rect is the _local(!) rect, so pygame.sprite.collidecrect can't be used
                if token.position_manager.get_global_rect().colliderect(self.rect):
                    found_tokens.add(token)
            self._tokens_in_last_frame = self._cached_tokens[1]
            # tokens_in_frame_and_last_frame = found_tokens.copy()
            found_tokens.add(self._tokens_in_last_frame)
            self._cached_tokens = (self.board.frame, found_tokens)
        return found_tokens

    def from_token(self, token: "token_mod.Token") -> None:
        if token.center:
            center = token.center
            width = self.board.width // 2
            height = self.board.height // 2
            self.topleft = (center[0] - width - token.width // 2, center[1] - height - token.height // 2)
        else:
            self.topleft = (0, 0)

    def _is_rect_in_viewport(self, rect):
        if rect[0] + rect[2] < 0 or rect[0] > self.get_viewport_width_in_pixels():
            return False
        if rect[1] + rect[3] < 0 or rect[1] > self.get_viewport_height_in_pixels():
            return False
        return True

    def is_token_repainted(self, token):
        return self.board.frame == 0 or self.is_token_in_viewport(token)

    def is_token_in_viewport(self, token):
        if token in self.get_tokens_in_viewport():
            return True
        else:
            return False


class TiledCameraManager(BoardCameraManager):
    def get_viewport_width_in_pixels(self):
        return self.viewport[0] * self.board.tile_size

    def get_viewport_height_in_pixels(self):
        return self.viewport[1] * self.board.tile_size


class HexCameraManager(BoardCameraManager):
    def get_viewport_width_in_pixels(self) -> int:
        """The width of the container"""
        return self.get_viewport_width() * self.board.get_tile_width() + 1 / 2 * self.board.get_tile_width()

    def get_viewport_height_in_pixels(self) -> int:
        """The height of the container"""
        return self.get_viewport_height() * self.board.get_tile_height() * 3 / 4 + self.board.get_tile_height() / 4
