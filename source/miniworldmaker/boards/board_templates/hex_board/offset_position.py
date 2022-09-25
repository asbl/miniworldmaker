import math

from miniworldmaker.positions import position as board_position
from miniworldmaker.boards.board_templates.hex_board import cube_coord


class OffsetPosition(board_position.Position):
    EVEN = 1
    ODD = -1

    def to_cube(self):
        if type(self.x) != int or type(self.y) != int:
            raise ValueError(f"x and y must be int. Found: {self.x}, {self.y} ; {type(self.x)}, {type(self.y)}")
        if self.y % 2 == 0:
            offset = OffsetPosition.EVEN
        else:
            offset = OffsetPosition.ODD
        q = self.x - (self.y - (self.y & 1)) // 2
        r = self.y
        return cube_coord.CubeCoord(q, r, -q - r)

    @classmethod
    def from_cube(cls, hex):
        x = hex.q + (hex.r - (hex.r & 1)) / 2.0
        y = hex.r
        return cls(x, y)

    def to_pixel(self, size=(0, 0), origin=(0, 0)):
        x = size[0] * math.sqrt(3) * (self.x + 0.5 * (self.y & 1)) + origin[0]
        y = size[1] * 3 / 2 * self.y + origin[1]
        return board_position.Position(x, y)

    def to_position(self):
        return board_position.Position(self.x, self.y)

    def on_the_board(self, board):
        if self.x < 0 or self.x >= board.columns or self.y < 0 or self.y >= board.rows:
            return False
        else:
            return True
