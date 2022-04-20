from collections import defaultdict
from typing import Union, Dict, Tuple

import pygame

import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.boards.board as board
import miniworldmaker.board_positions.tile_elements as tile_elements
import miniworldmaker.boards.token_connectors.tiled_board_connector as tiled_board_connector
from miniworldmaker.exceptions import miniworldmaker_exception
from miniworldmaker.exceptions.miniworldmaker_exception import TiledBoardTooBigError


class TiledBoard(board.Board):
    def __init__(self, columns: int = 20, rows: int = 16):
        """Initializes the TiledBoard

        Args:
            columns: The number of columns
            rows: The number of rows
        """
        self.default_token_speed: int = 1
        if columns > 1000 or rows > 1000:
            raise TiledBoardTooBigError(columns, rows, 40)
        super().__init__(columns=columns, rows=rows)
        self.tile_size = 40
        self.speed = 30
        self.dynamic_tokens_dict: defaultdict = defaultdict(list)  # the dict is regularly updated
        self.dynamic_tokens: set = set()  # Set with all dynamic actors
        self.static_tokens_dict: defaultdict = defaultdict(list)
        self.fixed_size = True
        self.rotatable_tokens = True
        self.tiles = defaultdict()
        self.corners = defaultdict()
        self.edges = defaultdict()
        self.setup_board()

    def setup_board(self):
        self.setup_tiles()
        self.setup_corners()
        self.setup_edges()

    def _templates(self):
        return tile_elements.Tile, tile_elements.Edge, tile_elements.Corner

    def add_tile_to_board(self, position):
        tile_cls, edge_cls, corner_cls = self._templates()
        tile_pos = board_position.Position(position[0], position[1])
        tile = tile_cls(tile_pos)
        self.tiles[tile.position] = tile

    def add_corner_to_board(self, position, direction):
        tile_cls, edge_cls, corner_cls = self._templates()
        corner = corner_cls(position, direction)
        corner_pos = corner.position
        if corner_pos not in self.corners:
            self.corners[corner_pos] = corner
        else:
            self.corners[corner_pos].merge(corner)

    def add_edge_to_board(self, position, direction):
        tile_cls, edge_cls, corner_cls = self._templates()
        edge = edge_cls(position, direction)
        edge_pos = edge.position
        if edge_pos not in self.edges:
            self.edges[edge_pos] = edge
        else:
            self.edges[edge_pos].merge(edge)

    def setup_tiles(self):
        for x in range(self.columns):
            for y in range(self.rows):
                self.add_tile_to_board((x, y))

    def setup_corners(self):
        tile_cls, edge_cls, corner_cls = self._templates()
        for position, tile in self.tiles.items():
            for direction in tile_cls.corner_vectors:
                self.add_corner_to_board(tile.position, direction)

    def setup_edges(self):
        tile_cls, edge_cls, corner_cls = self._templates()
        for position, tile in self.tiles.items():
            for direction in tile_cls.edge_vectors:
                self.add_edge_to_board(tile.position, direction)

    def get_tile(self, position):
        if self.is_tile(position):
            return self.tiles[(position[0], position[1])]
        else:
            raise miniworldmaker_exception.NoTileFoundError(position)

    def get_corner(self, position):
        if self.is_corner(position):
            return self.corners[(position[0], position[1])]
        else:
            raise miniworldmaker_exception.NoTileFoundError(position)

    def get_token_connector(self, token):
        return tiled_board_connector.TiledBoardConnector(self, token)

    def is_position_on_board(self, position: "board_position.Position") -> bool:
        position = board_position.Position.create(position)
        return self.position_manager.is_position_on_board(position)

    def borders(self, value: Union[tuple, "board_position.Position", pygame.Rect]) -> list:
        position = board_position.Position.create(value)
        return self.position_manager.get_borders_from_position(position)

    def _update_token_positions(self):
        """Updates the dynamic_tokens_dict.

        All positions of dynamic_tokens_dict are updated by reading the dynamic_tokens list.

        This method is called very often in self.sensing_tokens - The dynamic_tokens list should therefore be as small as possible.
        Other tokens should be defined as static.
        """
        self.dynamic_tokens_dict.clear()
        for token in self.dynamic_tokens:
            x, y = token.position[0], token.position[1]
            self.dynamic_tokens_dict[(x, y)].append(token)

    def sensing_tokens(self, position):
        if type(position) == tuple:
            position = board_position.Position(position[0], position[1])
        self._update_token_positions()  # This method can be a bottleneck!
        token_list = []
        if self.dynamic_tokens_dict[position[0], position[1]]:
            token_list.extend(self.dynamic_tokens_dict[(position[0], position[1])])
        if self.static_tokens_dict[position[1], position[1]]:
            token_list.extend(self.static_tokens_dict[(position[0], position[1])])
        token_list = [token for token in token_list]
        return token_list

    def sensing_token(self, position):
        token_list = self.sensing_tokens(position)
        if token_list is None or token_list == []:
            return None
        else:
            return token_list[0]

    @property
    def grid(self):
        """Displays grid overlay on background."""
        return self.background.grid

    @grid.setter
    def grid(self, value):
        self.background.grid = value

    def get_board_position(self, position):
        return board_position.Position.from_pixel(position)

    def draw_on_image(self, image, position):
        position = self.to_pixel(position)
        self.background.draw_on_image(image, position, self.tile_size, self.tile_size)

    def get_tile_from_pixel(self, position):
        return tile_elements.Tile.from_pixel(position)

    def get_edge_points(self) -> Dict[Tuple, "board_position.Position"]:
        edge_points = dict()
        for position, edge in self.edges.items():
            edge_points[position] = edge.to_pixel()
        return edge_points

    def get_corner_points(self) -> Dict[Tuple, "board_position.Position"]:
        corner_points = dict()
        for position, corner in self.corners.items():
            corner_points[position] = corner.to_pixel()
        return corner_points

    def is_edge(self, position):
        if position in self.edges:
            return True
        else:
            return False

    def is_corner(self, position):
        if position in self.corners:
            return True
        else:
            return False

    def is_tile(self, position):
        if position in self.tiles:
            return True
        else:
            return False

    def get_edge(self, position):
        if self.is_edge(position):
            return self.edges[(position[0], position[1])]
        else:
            raise miniworldmaker_exception.NoTileFoundError(position)

    def to_pixel(self, position, size=(0, 0), origin=(0, 0)):
        x = position[0] * self.tile_size + origin[0]
        y = position[1] * self.tile_size + origin[1]
        return board_position.Position(x, y)
