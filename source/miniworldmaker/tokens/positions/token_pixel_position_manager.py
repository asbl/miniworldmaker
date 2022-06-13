
import pygame

import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.tokens.positions.token_position_manager as token_positionmanager
from miniworldmaker.exceptions.miniworldmaker_exception import NoValidBoardPositionError


class PixelBoardPositionManager(token_positionmanager.TokenPositionManager):
    def __init__(self, token, board):
        super().__init__(token, board)
        self.size = (0, 0)
        self.set_position((0, 0))
        self.size=(40, 40)

    def get_rect(self) -> pygame.Rect:
        """Pixelboard-Rects are positioned at center of position
        """
        if self.token.costume:
            _rect = self.token.costume.image.get_rect()
        else:
            _rect = pygame.Rect(self.position[0], self._position[1], self.token.size[0], self.token.size[1])
        _rect_center_pos = super().get_position()
        _rect.center = _rect_center_pos[0], _rect_center_pos[1]
        return _rect

    def get_position(self):    
        shift_x = self.size[0] / 2
        shift_y = self.size[1] / 2
        rect_center = super().get_position()
        pos = rect_center[0] - shift_x, rect_center[1] - shift_y
        return board_position.Position.create(pos)
    
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

    def set_size(self, value):
        old_pos = self.get_position()
        super().set_size(value)
        self.set_position(old_pos)
        return self._size