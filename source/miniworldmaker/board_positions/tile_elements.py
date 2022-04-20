from typing import List, Dict
from collections import OrderedDict
import math
import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.tokens.token as token
import miniworldmaker.base.app as app


class TileBase:
    def __init__(self, position):
        self.int_coord = self._internal_coordinates()
        self.board = app.App.board
        self.position = self.int_coord.from_board_coordinates(position)
        self.positions = [(self.position)]

    @classmethod
    def from_pixel(cls, pixel_position) -> "TileBase":
        min_value = math.inf
        nearest_board_position = None
        for board_pos, pixel in cls.get_position_pixel_dict().items():
            distance = math.sqrt(pow(pixel_position[0] - pixel[0], 2) + pow(pixel_position[1] - pixel[1], 2))
            if distance < min_value:
                min_value = distance
                nearest_board_position = board_pos
        return cls.from_position(nearest_board_position)

    @staticmethod
    def get_local_center_coordinate():
        board = app.App.board
        return board_position.Position(board.tile_size / 2, board.tile_size / 2)

    @staticmethod
    def _internal_coordinates():
        return board_position.Position

    def to_pixel(self):
        pass

    def merge(self, other):
        assert other.position == self.position
        for pos in other.positions:
            if pos not in self.positions:
                self.positions.append(pos)

    def create_token(self):
        return token.Token(self.position)

    def get_tokens(self):
        tokens = []
        for tkn in self.board.tokens:
            if tkn.position == self.position:
                tokens.append(tkn)
        return tokens

    def add_token(self, token):
        token.position = self.position

    def get_neighbour_tiles(self) -> List["Tile"]:
        if hasattr(self, "_tiles") and self._tiles:  # cached at end of this function
            return self._tiles
        neighbours = []
        for tile, vectors in self.tile_vectors.items():
            for vector in vectors:
                if self.board.is_tile(self.position + vector):
                    neighbour = self.board.get_tile(self.position + vector)
                    if neighbour and neighbour not in neighbours:
                        neighbours.append(neighbour)
        self._tiles = neighbours
        return self._tiles


class TileDelimiter(TileBase):
    angles: Dict[str, tuple] = dict()
    direction_angles: Dict[str, int] = dict()

    def __init__(self, position, direction):
        super().__init__(position)
        internal_coordinates = self.int_coord.create(position)
        self.tile = self.board.get_tile(internal_coordinates)
        self.direction = self.direction_vectors()[direction]
        self.position = self.tile.position + self.direction
        self.positions = [(self.position, self.direction)]
        self.direction_str = direction
        self.angle = self.direction_angles[self.direction_str]

    @classmethod
    def get_direction_from_string(cls, direction_string):
        return cls.direction_vectors()[direction_string]

    def _get_direction_string(self, direction) -> str:
        if type(direction) == tuple:
            for dir_string, dir_vector in self.direction_vectors().items():
                if direction == dir_vector:
                    return dir_string
        else:
            raise TypeError("Direction must be tuple")

    def get_local_coordinate_for_tile(self, tile):
        tile_pos = tile.to_pixel()
        delimiter_pos = self.to_pixel()
        local = delimiter_pos - tile_pos
        return local

    def get_local_coordinate_for_base_tile(self) -> "board_position.Position":
        """Gets pixel offset based on tile

        Returns:
            Offset as position (x, y and y coordinate measured )
        """
        center = TileBase.get_local_center_coordinate()

        if self.angles:
            direction_tuple = self.direction
            direction = self._get_direction_string(direction_tuple)
            angle_nr = self.angles[direction]
            base_size = self.board.tile_size
            start_angle = self.start_angle()
            angle = 2.0 * math.pi * (start_angle - angle_nr) / len(self.angles)
            offset = board_position.Position(base_size / 2 * math.cos(angle), base_size / 2 * math.sin(angle))
            return offset + center
        else:
            return board_position.Position(0, 0) + center

    def to_pixel(self):
        local = self.get_local_coordinate_for_base_tile()
        tile_pos = self.tile.to_pixel()
        return tile_pos + local

    @staticmethod
    def direction_vectors():
        return None

    def start_angle(self):
        pass

    def get_angle(self, direction):
        return self.angles[direction]

    def get_direction(self):
        dir_str = self._get_direction_string(self.direction)
        return self.direction_angles[dir_str]


class Tile(TileBase):
    tile_vectors = {
        "w": (+1, 0),
        "nw": (+1, +1),
        "no": (-1, +1),
        "o": (-1, 0),
        "so": (-1, -1),
        "sw": (+1, -1),
    }

    corner_vectors = OrderedDict(
        [
            ("nw", (+0.5, +0.5)),
            ("no", (-0.5, +0.5)),
            ("so", (-0.5, -0.5)),
            ("sw", (+0.5, -0.5)),
        ]
    )

    edge_vectors = {
        "w": (-0.5, 0),
        "o": (+0.5, 0),
        "s": (0, +0.5),
        "n": (0, -0.5),
    }

    @classmethod
    def from_position(cls, position):
        board = app.App.board
        return board.get_tile(position)

    def __init__(self, position):
        super().__init__(position)
        self.tiles = []
        self.corners = []
        self.edges = []

    def get_neighbour_corners(self) -> List["Corner"]:
        if self.corners:
            return self.corners
        else:
            neighbours = []
            for corner, vector in self.corner_vectors.items():
                neighbour = self.board.get_corner(self.position + vector)
                if neighbour:
                    neighbours.append(neighbour)
            self.corners = neighbours
            return self.corners

    def to_pixel(self):
        x = self.position[0] * self.board.tile_size
        y = self.position[1] * self.board.tile_size
        return board_position.Position(x, y)

    @staticmethod
    def get_position_pixel_dict():
        board = app.App.board
        return board.get_center_points()

    def to_center(self):
        topleft = self.to_pixel()
        return topleft + self.get_local_center_coordinate()


class Corner(TileDelimiter):
    angles = {
        "no": 0,
        "nw": 1,
        "sw": 2,
        "so": 3,
    }

    direction_angles = {
        "no": 0,
        "nw": 0,
        "sw": 0,
        "so": 0,
    }

    @staticmethod
    def direction_vectors():
        return Tile.corner_vectors

    @classmethod
    def from_position(cls, position):
        board = app.App.board
        return board.get_corner(position)

    @classmethod
    def from_pixel(cls, position):
        board = app.App.board
        min_value = math.inf
        nearest_hex = None
        corner_points = board.get_corner_points()
        for corner_position, corner_pos in corner_points.items():
            distance = math.sqrt(pow(position[0] - corner_pos[0], 2) + pow(position[1] - corner_pos[1], 2))
            if distance < min_value:
                min_value = distance
                nearest_hex = corner_position
        return cls.from_position(nearest_hex)

    @classmethod
    def from_tile(cls, position, direction_string):
        board = app.App.board
        tile = board.get_tile(position)
        return board.get_corner(tile.position + cls.get_direction_from_string(direction_string))

    def start_angle(self):
        return 0.5


class Edge(TileDelimiter):
    tile_vectors = {
        "w": [(-0.5, 0), (0.5, 0)],
        "n": [(0, 0.5), (0, -0.5)],
        "o": [(-0.5, 0), (0.5, 0)],
        "s": [(0, 0.5), (0, -0.5)],
    }

    direction_angles = {
        "o": 0,
        "s": 90,
        "w": 0,
        "n": 90,
    }

    angles = {
        "o": 0,
        "s": 1,
        "w": 2,
        "n": 3,
    }

    @staticmethod
    def direction_vectors():
        return Tile.edge_vectors

    @staticmethod
    def get_position_pixel_dict():
        board = app.App.board
        return board.get_edge_points()

    @classmethod
    def from_position(cls, position):
        board = app.App.board
        return board.get_edge(position)

    def start_angle(self):
        return 0
