from miniworldmaker.boards.elements import tile_elements
from miniworldmaker.app import app
from miniworldmaker.board_positions import board_position
from miniworldmaker.boards import hex_board
import math
import collections
import numpy as np

class HexTile(tile_elements.Tile):

    tile_vectors = {
        "w": (+1, 0, -1),
        "nw": (+1, -1, 0),
        "no": (0, -1, +1),
        "o": (-1, 0, +1),
        "so": (-1, +1, 0),
        "sw": (0, +1, -1),
    }

    corner_vectors = {
        "n": (+1, 0, +1),
        "nw": (+1, 0, 0),
        "no": (0, 0, +1),
        "sw": (+1, +1, 0),
        "so": (0, +1, +1),
        "s": (0, +1, 0),
    }

    edge_vectors = {
            "w": [1, 0.5, 0],
            "nw" : [1, 0, 0.5],
            "no": [0.5,0,1],
            "o": [0,0.5,1],
            "so": [0.5,1,0.5],
            "sw": [0.5,1,0]}
    
    def __init__(self, position):
        self.offset = OffsetPosition(position[0], position[1])
        self.board = app.App.board
        self.position = self.offset.to_cube()
        self.tiles = []
        self.corners = []
        self.edges = []
        self.board : "hex_board.HexBoard" = app.App.board

    def to_center(self):
        center_offset = self.get_center_offset()
        return self.position.to_pixel(size=(self.board.get_hex_size()[1], self.board.get_hex_size()[1]), origin=center_offset)

    @staticmethod
    def get_center_offset():
        board = app.App.board
        return board_position.Position(board.get_tile_width() / 2, board.get_tile_height() / 2)

    def to_pixel(self):
        return self.position.to_pixel(size=(self.board.get_hex_size()[1], self.board.get_hex_size()[1]), origin=(0,0))

    #@classmethod
    #def from_pixel(cls, pixel_position, board):
    #    q = (math.sqrt(3) / 3 * pixel_position[0] - 1.0 / 3 * pixel_position[1]) / (board.base_size() / 2)
    #    r = (2.0 / 3 * pixel_position[1]) / (board.base_size() / 2)
    #    cube_coord = OffsetPosition.from_cube(CubeCoord(q, r, -q - r).round())
    #    return board.tiles[cube_coord]

    @classmethod
    def from_pixel(cls, position):
        board : "hex_board.HexBoard"= app.App.board
        min_value = math.inf
        nearest_hex = None
        center_points = board.get_center_points()
        for hex_position, hex_center in center_points.items():
            distance = math.sqrt(pow(position[0] - hex_center[0], 2) + pow(position[1] - hex_center[1], 2))
            if distance < min_value:
                min_value = distance
                nearest_hex = hex_position
        return HexTile(nearest_hex)

    def is_in_tile(self, pixel_position):
        distance = distance(pixel_position, self.to_center())
        for neighbour in self.get_neighbours():
            if distance(pixel_position, neighbour.to_center()) > distance:
                return False
        return True

    def get_corner(self, direction):
        board = app.App.board
        if type(direction) == str:
            vector = self.corner_vectors[direction]
        else:
            vector = direction
        return self.board.get_corner(self.position + vector)

    def __str__(self):
        return f"Hex-Tile at {self.position}"

class HexCorner():

    angles = {"n": 2,
                  "no" : 3,
                  "so": 4,
                  "s": 5,
                  "sw": 0,
                  "nw": 1}

    start_angle = 0.5


    neighbours = {
        "n": ["nw", "no"],
        "no": ["no", "o"],
        "nw": ["nw", "w"],
        "sw": ["sw", "w"],
        "so": ["so", "o"],
        "s": ["so", "sw"],
                }

    
    def __init__(self, position, direction):        
        self.position = CubeCoord.from_position(position) + HexTile.corner_vectors[direction]
        self.positions = [(position, direction)]
        self.key = (self.position.q,self.position.r, self.position.s)
        self.board = app.App.board

    @classmethod
    def from_positions(self, p1, p2, p3):
        pass

    def get_neighbour_tiles(self):
        pass

    def get_neighbour_corners(self):
        pass

    def get_neighbour_edges(self):
        pass

    def get_position(self):
        position = self.positions[0][0]
        direction = self.positions[0][1]
        return self._get_position(position, direction)
        #return self.cube_coord.to_pixel(size = (self.board.get_hex_size()[0], self.board.get_hex_size()[1]), origin = (0,0))

    def _get_offset(self, direction):
        angle = HexCorner.angles[direction]
        start_angle = self.start_angle
        base_size = self.board.base_size()
        angle = 2.0 * math.pi * (start_angle - angle) / 6.0
        return board_position.Position(base_size / 2 * math.cos(angle), base_size / 2 * math.sin(angle))
    
    def _get_position(self, position, direction):
        offset = self._get_offset(direction)
        center = HexTile.get_center_offset()
        corner = self.board._hex_to_pixel(position, offset + center)
        return corner

    def __eq__(self, __o: object) -> bool:
        if type(__o) == HexCorner and self.position == __o.position:
            return True
        else:
            return False

    def merge(self, corner):
        assert corner.position == self.position
        for pos in corner.positions:
            if pos not in self.positions:
                self.positions.append(pos)

    def __str__(self) -> str:
        corner_str =  "Corner at"
        for position in self.positions:
            corner_str+= f"({position[0]}, {position[1]})"
        return corner_str
    

class HexEdge():
    def __init__(self, position, direction):
        self.position = CubeCoord.from_position(position) + HexTile.edge_vectors[direction]
        self.positions = [(position, direction)]
        self.key = (self.position.q,self.position.r, self.position.s)

    def merge(self, edge):
        assert edge.position == self.position
        for pos in edge.positions:
            if pos not in self.positions:
                self.positions.append(pos)


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
        return board_position.Position(round(coord.item(0) * size[0] + origin[0]), round(coord.item(1) * size[1] + origin[1]))

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
    def from_position(cls, position):
        return OffsetPosition(position[0], position[1]).to_cube()

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

    def to_pixel(self, size, origin):
        x = size[0] * math.sqrt(3) * (self.x + 0.6 * (self.y & 1)) + origin[0]
        y = size[1] * 3 / 2 * self.y + origin[1]
        return board_position.Position(x, y)

    def to_position(self):
        return board_position.Position(self.x, self.y)

    def on_board(self, board):
        if self.x<0 or self.x >= board.columns or self.y<0 or self.y >= board.rows:
            return False
        else:
            return True