from miniworldmaker.board_positions import board_position
from miniworldmaker.app import app
from typing import List

class Tile:

    tile_vectors = {
        "w": (+1, 0),
        "nw": (+1, +1),
        "no": (-1, +1),
        "o": (-1, 0),
        "so": (-1, -1),
        "sw": (+1, -1),
    }

    corner_vectors = {
        "w": (+1, 0),
        "nw": (+1, +1),
        "no": (-1, +1),
        "o": (-1, 0),
        "so": (-1, -1),
        "sw": (+1, -1), 
    }

    edge_vectors = {}

    def __init__(self, position):
        self.position = position
        self.corners = []
        self.edges = []

    def get_neighbour_tiles(self) -> List["Tile"]:
        if self.tiles:
            return self.tiles
        else: # fill tiles
            neighbours = []
            for tile, vector in self.neighbour_tiles.items():
                neighbour = self.board.get_tile(self.position + vector)
                if neighbour:
                    neighbours.append(neighbour)
            self.tiles = neighbours
            return self.tiles

    def get_neighbour_tiles(self) -> List["Corner"]:
        if self.corners:
            return self.corners
        else: # fill tiles
            neighbours = []
            for tile, vector in self.corners.items():
                neighbour = self.board.get_corner(self.position + vector)
                if neighbour:
                    neighbours.append(neighbour)
            self.corners = neighbours
            return self.corners

    def get_neighbour(self, vector):
        pass

    def get_edge(self, vector):
        pass

    def get_neighbours_dict(self):
        pass # "nw"-> Tile

    def is_in_tile(pixel):
        pass

    @classmethod
    def from_pixel(cls, position):
        board = app.App.board
        column = (position[0] // board.tile_size)
        row = (position[1] // board.tile_size)
        return column, row

    def to_pixel(self, position):
        board = self.board
        x = position[0] * board.tile_size
        y = position[1] * board.tile_size
        return x, y

class Corner:
    def __init__(self, position, direction):     
        self.position = (0,0)
        self.positions = [(position, direction)]

    def merge(self, corner):
        assert corner.position == self.position
        for pos in corner.positions:
            if pos not in self.positions:
                self.positions.append(pos)

class Edge:
    def __init__(self, position, direction):     
        self.position = (0,0)
        self.positions = [(position, direction)]

    def merge(self, corner):
        assert corner.position == self.position
        for pos in corner.positions:
            if pos not in self.positions:
                self.positions.append(pos)