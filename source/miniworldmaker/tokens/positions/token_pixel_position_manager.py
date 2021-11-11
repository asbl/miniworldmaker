import miniworldmaker.tokens.positions.token_position_manager as token_positionmanager
import pygame
from miniworldmaker.board_positions import board_position
from miniworldmaker.board_positions import board_position_factory

class PixelBoardPositionManager(token_positionmanager.TokenPositionManager):
    def __init__(self, token, position):
        super().__init__(token, position)
        self.size = (0, 0)
        if position:
            self.set_position(position)
        else:
            self.set_position((0, 0))
        self.size=(40, 40)

    @property
    def rect(self) -> pygame.Rect:
        """
        Pixelboard-Rects are positioned at center of position
        """
        if self.token.costume:
            _rect = self.token.image.get_rect()
            _rect.center = self._position[0], self._position[1]
            return _rect
        else:
            return pygame.Rect(self._position[0], self._position[1], self.size[0], self.size[1])

    def get_position(self):    
        shift_x = self.size[0] / 2
        shift_y = self.size[1] / 2
        rect_center = super().get_position()
        pos = rect_center[0] - shift_x, rect_center[1] - shift_y
        return board_position_factory.BoardPositionFactory(self.token.board).create(pos)
    
    def set_position(self, value):
        """
        Because Pixelboard-Rects are positioned at center of position, newly created Objects are shifted down right.

        """
        if value:
            shift_x = self.size[0] / 2.0
            shift_y = self.size[1] / 2.0
            pos = (value[0] + shift_x, value[1] + shift_y)
            return super().set_position(pos)
        else:
            raise Exception("Position must not be none!")

    def get_center(self):
        return super().get_position()

    def set_center(self, value):
        return super().set_position(value)

    def set_size(self, value):
        old_pos = self.get_position()
        super().set_size(value)
        self.set_position(old_pos)
        return self._size