import pygame

import miniworldmaker.positions.position as board_position
import miniworldmaker.tokens.managers.token_position_manager as token_positionmanager
from miniworldmaker.exceptions.miniworldmaker_exception import NoValidBoardPositionError


class PixelBoardPositionManager(token_positionmanager.TokenPositionManager):
    def __init__(self, token, board):
        super().__init__(token, board)
        self._position = (0, 0)
        self._size = (40, 40)

    def get_local_rect(self) -> pygame.Rect:
        """Pixelboard-Rects are positioned at center of position
        """
        _rect = self.get_global_rect()
        _rect.topleft = self.token.board.camera.get_local_position(_rect)
        return _rect

    def get_global_rect(self) -> pygame.Rect:
        """Pixelboard-Rects are positioned at center of position
        """
        _rect = super().get_global_rect()
        _rect_center = self.center
        # board position without shift is the center position
        _rect.center = _rect_center
        return _rect

    def get_position(self):
        shift_x = self.size[0] / 2
        shift_y = self.size[1] / 2
        rect_center = super().get_position()
        pos = rect_center[0] - shift_x, rect_center[1] - shift_y
        return board_position.Position.create(pos)

    @property
    def center_x(self):
        """x-value of token center-position"""
        return self._position[0]

    @center_x.setter
    def center_x(self, value):
        self.set_center((value, self.center_y))

    @property
    def center_y(self):
        """y-value of token center-position"""
        return self._position[1]

    @center_y.setter
    def center_y(self, value):
        self.set_center((self.center_x, value))

    def set_position(self, value):
        """Because Pixelboard-Rects are positioned at center of position, newly created Objects are shifted down right.

        """
        if value:
            shift_x = self.size[0] / 2.0
            shift_y = self.size[1] / 2.0
            pos = (value[0] + shift_x, value[1] + shift_y)
            return super().set_position(pos)
        else:
            raise NoValidBoardPositionError(value)

    def get_center(self):
        # Default position is center
        return super().get_center()

    def set_center(self, value):
        # Default position is center
        super().set_position((value[0], value[1]))

    def set_size(self, value, scale=False):
        old_pos = self.get_position()
        super().set_size(value, scale)
        self.set_position(old_pos)
        return self._size
