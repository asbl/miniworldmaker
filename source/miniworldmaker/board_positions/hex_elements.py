from collections import OrderedDict
from miniworldmaker.base import app
from miniworldmaker.board_positions import tile_elements
from miniworldmaker.board_positions import board_position

import collections
from typing import Union, List
import math
import numpy as np
import miniworldmaker.board_positions.board_position as board_position

class HexBase(tile_elements.TileBase):
    @staticmethod
    def get_local_center_coordinate() -> "board_position.BoardPosition":
        """Gets the local center coordinate of each tile.
        """
        board = app.App.board
        return board_position.Position(board.get_tile_width() / 2, board.get_tile_height() / 2)

    def _internal_coordinates(self):
        return CubeCoord

    def _external_coordinates(self):
        return CubeCoord


class HexTile(HexBase, tile_elements.Tile):
    tile_vectors = {
        "w": (+1, 0, -1),
        "nw": (+1, -1, 0),
        "no": (0, -1, +1),
        "o": (-1, 0, +1),
        "so": (-1, +1, 0),
        "sw": (0, +1, -1),
    }

    corner_vectors = OrderedDict(
        [
            ("n", (+1, 0, +1)),
            ("nw", (+1, 0, 0)),
            ("sw", (+1, +1, 0)),
            ("s", (0, +1, 0)),
            ("so", (0, +1, +1)),
            ("no", (0, 0, +1)),
        ]
    )

    edge_vectors = {
        "w": (1, 0.5, 0),
        "no": (1, 0, 0.5),
        "nw": (0, -1, -0.5),
        "o": (0, 0.5, 1),
        "so": (0.5, 1, 0),
        "sw": (0.5, 1, 0.5),
    }

    def is_in_tile(self, pixel_position : "board_position.BoardPosition") -> bool:
        """Returns True, if coordinate is in tile.
        :param pixel_position: board position in pixels
        :return: True, if coordinate is in tile
        """
        distance = self.distance(pixel_position, self.to_center())
        for neighbour in self.get_neighbours():
            if distance(pixel_position, neighbour.to_center()) > distance:
                return False
        return True

    def get_corner(self, direction: Union[str, tuple]) -> "CubeCoord":
        """Gets corner by direction
        :param direction: A string (e.g. nw, for north-west corner) or a direction-vector
        :return: The corner.
        """
        if type(direction) == str:
            vector = self.corner_vectors[direction]
        else:
            vector = direction
        return self.board.get_corner(self.position + vector)

    def __str__(self):
        return f"Hex-Tile at {self.position}"

    def to_pixel(self) -> "board_position.BoardPosition":
        """gets topleft position of tile
        """
        return self.int_coord.to_pixel(
            self.position, (self.board.get_tile_width() / 2, self.board.get_tile_height() / 2), (0, 0)
        )

    def _internal_coordinates(self):
        return CubeCoord

    def _external_coordinates(self):
        return CubeCoord

    def __eq__(self, other):
        if self.position == other.position:
            return True
        else:
            return False


class HexCorner(HexBase, tile_elements.Corner):
    angles = {"n": 2, "no": 3, "so": 4, "s": 5, "sw": 0, "nw": 1}
    direction_angles = {"n": 0, "no": 0, "so": 0, "s": 0, "sw": 0, "nw": 0}

    tile_vectors = {
        "n": [(-1, -1, 0), (0, -1, -1), (-1, 0, -1)],
        "nw": [(0, -1, 0), (0, 0, -1), (-1, 0, 0)],
        "sw": [(-1, 0, -1), (0, -1, -1), (-1, -1, 0)],
        "s": [(0, -1, 0), (0, 0, -1), (-1, 0, 0)],
        "so": [(-1, -1, 0), (-1, 0, -1), (0, -1, -1)],
        "no": [(0, -1, 0), (0, 0, -1), (-1, 0, 0)],
    }

    corner_vectors = {
        "n": [(0, -1, 0), (-1, 0, 0), (0, 0, -1)],
        "nw": [(0, 0, 1), (0, 1, 0), (0, 0, 1)],
        "sw": [(0, -1, 0), (0, -1, 0), (0, 0, -1)],
        "s": [(0, 1, 0), (0, 1, 0), (1, 0, 0)],
        "so": [(0, -1, 0), (-1, 0, 0), (0, 0, -1)],
        "no": [(1, 0, 0), (0, 1, 0), (0, 0, 1)],
    }

    def __eq__(self, __o: object) -> bool:
        if type(__o) == HexCorner and self.position == __o.position:
            return True
        else:
            return False

    def __str__(self) -> str:
        corner_str = "Corner at"
        for position in self.positions:
            corner_str += f"({position})"
        return corner_str

    def _internal_coordinates(self):
        return CubeCoord

    def _external_coordinates(self):
        return CubeCoord

    @staticmethod
    def direction_vectors():
        return HexTile.corner_vectors


class HexEdge(HexBase, tile_elements.Edge):
    tile_vectors = {
        "w": [(-1, 0.5, 0), (0, 0.5, -1)],
        "sw": [(-0.5, 1, 0), (-0.5, 0, 1)],
        "so": [(1, 0, 0.5), (0, 1, 0.5)],
        "o": [(-1, -0.5, 0), (0, -0.5, -1)],
        "no": [(-0.5, 1, 0), (-0.5, 0, 1)],
        "nw": [(1, 0, 0.5), (0, 1, 0.5)],
    }

    corner_vectors = {
        "w": [(0, -0.5, 0), (0, 0.5, 0)],
        "sw": [(0.5, 0, 0), (-0.5, 0, 0)],
        "so": [(0, 0, 0.5), (0, 0, -0.5)],
        "o": [(0, -0.5, 0), (0, 0.5, 0)],
        "no": [(0.5, 0, 0), (-0.5, 0, 0)],
        "nw": [(0, 0, 0.5), (0, 0, -0.5)],
    }

    direction_angles = {"o": 0, "so": -60, "sw": 60, "w": 0, "nw": -60, "no": 60}

    angles = {"o": 3, "so": 4, "sw": 5, "w": 0, "nw": 1, "no": 2}

    def __str__(self) -> str:
        edge_str = "Edge at"
        for position in self.positions:
            edge_str += f"({position})"
        return edge_str

    @classmethod
    def from_tile(cls, tile:"board_position.BoardPosition", direction:str) -> "HexEdge":
        """
        gets a Edge from tile-position and direction
        :param tile: External coordinates for tile
        :param direction: direction as string.
        :return: the HexEdge
        """
        return HexEdge(tile, direction)

    @staticmethod
    def direction_vectors():
        return HexTile.edge_vectors

    def _internal_coordinates(self):
        return CubeCoord

    def _external_coordinates(self):
        return CubeCoord


class CubeCoord(collections.namedtuple("Hex", ["q", "r", "s"])):
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
        return OffsetPosition.from_cube(self)

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
        return OffsetPosition.from_board_coordinates(position).to_cube()

    @classmethod
    def create(cls, position):
        if type(position) == tuple and len(position) == 2:
            return OffsetPosition(position[0], position[1]).to_cube()
        elif isinstance(position, board_position.Position):
            return OffsetPosition(position[0], position[1]).to_cube()
        elif isinstance(position, CubeCoord):
            return position
        else:
            raise TypeError(f"position is {type(position)}, should be OffsetPosition, Position or CubeCoord")


class OffsetPosition(board_position.Position):
    EVEN = 1
    ODD = -1

    def to_cube(self):
        if self.y % 2 == 0:
            offset = OffsetPosition.EVEN
        else:
            offset = OffsetPosition.ODD
        q = self.x - (self.y - (self.y & 1)) / 2
        r = self.y
        return CubeCoord(q, r, -q - r)

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

    def on_board(self, board):
        if self.x < 0 or self.x >= board.columns or self.y < 0 or self.y >= board.rows:
            return False
        else:
            return True
