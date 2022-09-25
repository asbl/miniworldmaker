import collections
import math

import numpy as np

from miniworldmaker.positions import position as board_position
from miniworldmaker.boards.board_templates.hex_board import offset_position


class CubeCoord(collections.namedtuple("Hex", ["q", "r", "s"]), board_position.PositionBase):
    matrix = np.matrix([[math.sqrt(3.0), math.sqrt(3.0) / 2.0], [0.0, 3.0 / 2.0]])
    inverse = np.matrix([[math.sqrt(3.0) / 3.0, -1.0 / 3.0], [0.0, 2.0 / 3.0]])

    def __add__(self, vec):
        return CubeCoord(self.q + vec[0], self.r + vec[1], self.s + vec[2])

    def __sub__(self, vec):
        return CubeCoord(self.q - vec[0], self.r - vec[1], self.s - vec[2])

    def neighbours(self):
        neighbours = []
        for direction, direction_vector in CubeCoord.direction_vectors.items():
            neighbour = self + direction_vector
            neighbours.append(neighbour)
        return neighbours

    def distance(self, other):
        other = CubeCoord.create(other)
        vec = self - other
        return (abs(vec.q) + abs(vec.r) + abs(vec.s)) / 2

    def round(self):
        qi = int(round(self.q))
        ri = int(round(self.r))
        si = int(round(self.s))
        q_diff = abs(qi - self.q)
        r_diff = abs(ri - self.r)
        s_diff = abs(si - self.s)
        if q_diff > r_diff and q_diff > s_diff:
            qi = -ri - si
        else:
            if r_diff > s_diff:
                ri = -qi - si
            else:
                si = -qi - ri
        return CubeCoord(qi, ri, si)

    def to_pixel(self, size, origin):
        matrix = self.matrix
        cube_vector = np.array([[self.q, self.r]])
        coord = matrix.dot(cube_vector.T)
        return board_position.Position(
            coord.item(0) * size[1] + origin[0], coord.item(1) * size[1] + origin[1]
        )

    def to_offset(self):
        return offset_position.OffsetPosition.from_cube(self)

    @classmethod
    def from_pixel(cls, position, size):
        inverse_matrix = CubeCoord.inverse_matrix
        cube_vector = np.array([[position[0], position[1]]])
        coord = inverse_matrix.dot(cube_vector.T)
        q = coord.item(0) / size[0]
        r = coord.item(1) / size[1]
        return CubeCoord(q, r, -q - r)

    @classmethod
    def from_board_coordinates(cls, position):
        return offset_position.OffsetPosition.from_board_coordinates(position).to_cube()

    @classmethod
    def create(cls, position):
        if type(position) == tuple and len(position) == 2:
            return offset_position.OffsetPosition(position[0], position[1]).to_cube()
        elif isinstance(position, board_position.Position):
            return offset_position.OffsetPosition(position[0], position[1]).to_cube()
        elif isinstance(position, CubeCoord):
            return position
        else:
            raise TypeError(f"position is {type(position)}, should be OffsetPosition, Position or CubeCoord")

    def __str__(self):
        return f"q: {self.q} r: {self.r} s: {self.s}"
