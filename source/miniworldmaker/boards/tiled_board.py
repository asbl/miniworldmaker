from collections import defaultdict
from typing import Union, Dict, Tuple, Optional

import pygame

import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.board_positions.tile_elements as tile_elements
import miniworldmaker.board_positions.tile_factory as tile_factory
import miniworldmaker.boards.board as board
import miniworldmaker.boards.token_connectors.tiled_board_connector as tiled_board_connector
from miniworldmaker.exceptions import miniworldmaker_exception
from miniworldmaker.exceptions.miniworldmaker_exception import TiledBoardTooBigError


class TiledBoard(board.Board):
    """
    A TiledBoard is a Board where each Token is placed in one Tile.

    With Tiled Board, you can realize RPGs and Boardgames.

    .. image:: /_images/rpg.jpg
        :width: 100%
        :alt: TiledBoard

    Each Token on a TiledBoard can be placed on a Tile, on a Corner between Tiles or on an Edge between Tiles.

    Examples:

        Create Token on Tile, Corner and Edge:

        .. code-block::

            from miniworldmaker import *
            board = TiledBoard(6, 3)
            board.grid = True
            last_corner = None

            tile = Tile((1,1))
            t1 = tile.create_token()
            t1.fill_color = (255,255,255)

            corner = Corner((3,1), "nw")
            t2 = corner.create_token()
            t2.fill_color = (255,0,0)

            edge = Edge((5,1), "w")
            t3 = edge.create_token()
            t3.fill_color = (0,0,255)
            t3.size = (0.2,1)
            t3.direction = edge.angle

            board.run()


        .. image:: /_images/tilecorneredge.png
            :alt: Placing Tokens on a Tile, on a Corner or in a Edge
    """

    def __init__(self, columns: int = 20, rows: int = 16, empty=False):
        """Initializes the TiledBoard

        Args:
            columns: The number of columns
            rows: The number of rows
            empty: The board has no tiles, edges, and corners. They must be created manually
        """
        self.default_token_speed: int = 1
        if columns > 1000 or rows > 1000:
            raise TiledBoardTooBigError(columns, rows, 40)
        super().__init__(columns=columns, rows=rows)
        self.tile_factory = self._get_tile_factory()
        self.tile_size = 40
        self.speed = 20
        self.dynamic_tokens_dict: defaultdict = defaultdict(list)  # the dict is regularly updated
        self.dynamic_tokens: set = set()  # Set with all dynamic actors
        self.static_tokens_dict: defaultdict = defaultdict(list)
        self.tokens_fixed_size = True
        self.rotatable_tokens = True
        self.empty = empty
        self.tiles = defaultdict()
        self.corners = defaultdict()
        self.edges = defaultdict()
        self.setup_board()

    def _get_tile_factory(self):
        return tile_factory.TileFactory()

    def clear_tiles(self):
        """Removes all tiles, coners and edges from Board

        Instead of clearing the board, you can add the parameter empty to Board to create a new Board from scratch.

        Examples:

            Clear and re-create board:

            .. code-block:: python

                from miniworldmaker import *
                board = HexBoard(8, 8)

                @board.register
                def on_setup(self):
                    self.clear_tiles()
                    center = HexTile((4, 4))
                    for x in range(self.columns):
                        for y in range(self.rows):
                            if center.position.distance((x, y)) < 2:
                                tile = self.add_tile_to_board((x, y))
                                tile.create_token()


                board.run()


            Create a new board from scratch

            .. note::

                This variant is faster, because Tiles are not created twice

            .. code-block:: python

                from miniworldmaker import *
                board = HexBoard(8, 8, empty=True)

                @board.register
                def on_setup(self):
                    center = HexTile((4, 4))
                    for x in range(self.columns):
                        for y in range(self.rows):
                            if center.position.distance((x, y)) < 2:
                                tile = self.add_tile_to_board((x, y))
                                tile.create_token()


                board.run()
        """
        self.tiles.clear()
        self.corners.clear()
        self.edges.clear()

    def setup_board(self):
        """In this method, corners and edges are created.
        """
        if not self.empty:
            self._setup_tiles()
            self._setup_corners()
            self._setup_edges()

    def _templates(self):
        """Returns Classes for Tile, Edge and Corner
        """
        return tile_elements.Tile, tile_elements.Edge, tile_elements.Corner

    def add_tile_to_board(self, position):
        tile_cls, edge_cls, corner_cls = self._templates()
        tile_pos = board_position.Position(position[0], position[1])
        tile = tile_cls(tile_pos)
        self.tiles[tile.position] = tile
        return tile

    def add_corner_to_board(self, position, direction):
        tile_cls, edge_cls, corner_cls = self._templates()
        corner = corner_cls(position, direction)
        corner_pos = corner.position
        if corner_pos not in self.corners:
            self.corners[corner_pos] = corner
        else:
            self.corners[corner_pos].merge(corner)
        return self.corners[corner_pos]

    def add_edge_to_board(self, position, direction):
        edge_cls = self.tile_factory.edge_cls
        edge = edge_cls(position, direction)
        edge_pos = edge.position
        if edge_pos not in self.edges:
            self.edges[edge_pos] = edge
        else:
            self.edges[edge_pos].merge(edge)
        return self.edges[edge_pos]

    def _setup_tiles(self):
        """Adds Tile to Board for each BoardPosition
        """
        for x in range(self.columns):
            for y in range(self.rows):
                self.add_tile_to_board((x, y))

    def _setup_corners(self):
        """Add all Corner to Board for each Tile.

        Merges identical corners for different Tiles
        """
        tile_cls = self.tile_factory.tile_cls
        corner_cls = self.tile_factory.corner_cls
        for position, tile in self.tiles.items():
            for direction in tile_cls.corner_vectors:
                self.add_corner_to_board(tile.position, direction)

    def _setup_edges(self):
        """Add all Edges to Board for each Tile

        Merges identical edges for different tiles
        """
        tile_cls = self.tile_factory.tile_cls
        edge_cls = self.tile_factory.edge_cls
        for position, tile in self.tiles.items():
            for direction in tile_cls.edge_vectors:
                self.add_edge_to_board(tile.position, direction)

    def get_tile(self, position: board_position):
        """Gets Tile at Position.

        Raises TileNotFoundError, if Tile does not exists.

        Examples:

            Get tile from token:

            .. code-block:: python

                tile = board.get_tile(token.position)

            Full example:

            .. code-block:: python

                from miniworldmaker import *

                board = TiledBoard(6, 3)
                board.grid = True
                last_corner = None

                tile = Tile((1,1))
                t1 = tile.create_token()
                t1.fill_color = (255,255,255)

                tile=board.get_tile((1,1))
                assert(tile.get_tokens()[0] == t1)

                board.run()

        :param position: Position on Board
        :return: Tile on Posiiton, if position exists
        """
        if self.is_tile(position):
            return self.tiles[(position[0], position[1])]
        else:
            raise miniworldmaker_exception.TileNotFoundError(position)

    def get_corner(self, position: board_position.Position, direction: Optional[str] = None):
        """Gets Corner at Position.

        Raises CornerNotFoundError, if Tile does not exists.

        Examples:

            Get corner from token:

            .. code-block:: python

                corner = board.get_corner(token.position)

            Get corner from board-position and direction

            .. code-block:: python

                from miniworldmaker import *

                from miniworldmaker import *
                board = TiledBoard(6, 3)
                board.grid = True
                last_corner = None

                corner = Corner((3,1), "nw")
                t2 = corner.create_token()
                t2.fill_color = (255,0,0)

                corner=board.get_corner((3,1),"nw")
                assert(corner.get_tokens()[0] == t2)

                board.run()

        :param position: Position on Board
        :param direction: if direction is not None, position is interpreted as tile-board-position
        :return: Corner on Posiiton, if position exists
        """
        corner_cls = self.tile_factory.corner_cls
        if direction is not None:
            position = corner_cls(position, direction).position
        if self.is_corner(position):
            return self.corners[(position[0], position[1])]
        else:
            raise miniworldmaker_exception.CornerNotFoundError(position)

    def get_edge(self, position, direction: Optional[str] = None):
        """Gets Edge at Position.

        Raises EdgeNotFoundError, if Tile does not exists.

        Examples:

            Get edge from token:

            .. code-block:: python

                tile = board.get_edge(token.position)

            Get edge from board-position and direction

            .. code-block:: python

                from miniworldmaker import *
                board = TiledBoard(6, 3)
                board.grid = True
                last_corner = None

                t3 = edge.create_token()
                t3.fill_color = (0,0,255)
                t3.size = (0.2,1)
                t3.direction = edge.angle

                edge=board.get_edge((5,1),"w")
                assert(edge.get_tokens()[0] == t3)

                board.run()

        :param position: Position on Board
        :return: Edge on Posiiton, if position exists
        """
        edge_cls = self.tile_factory.edge_cls
        if direction is not None:
            position = edge_cls(position, direction).position
        if self.is_edge(position):
            return self.edges[(position[0], position[1])]
        else:
            raise miniworldmaker_exception.TileNotFoundError(position)

    @staticmethod
    def _get_token_connector_class():
        return tiled_board_connector.TiledBoardConnector

    def is_position_on_board(self, position: "board_position.Position") -> bool:
        """
        Returns True if a position is on board.
        """
        position = board_position.Position.create(position)
        return self.position_manager.is_position_on_board(position)

    def borders(self, value: Union[tuple, "board_position.Position", pygame.Rect]) -> list:
        """
        Returns the Board's borders, if token is near a Border.
        """
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
        """Sensing tokens at same position
        """
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
        """Sensing single token at same position

        Faster than sensing_tokens, but only the first found token is recognized.
        """
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

    def draw_on_image(self, image, position):
        position = self.to_pixel(position)
        self.background.draw_on_image(image, position, self.tile_size, self.tile_size)

    def get_from_pixel(self, position):
        """Gets board position from pixel coordinates
        """
        if position[0] > self.container_width or position[1] > self.container_height:
            return None
        else:
            return self.get_tile_from_pixel(position).position

    get_board_position_from_pixel = get_from_pixel
    
    def get_tile_from_pixel(self, position):
        """Gets nearest Tile from pixel
        """
        tile_cls = self.tile_factory.tile_cls
        return tile_cls.from_pixel(position)

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
        """Returns True, if position is a edge.
        """
        if position in self.edges:
            return True
        else:
            return False

    def is_corner(self, position):
        """Returns True, if position is a corner.
        """
        if position in self.corners:
            return True
        else:
            return False

    def is_tile(self, position):
        """Returns True, if position is a tile.
        """
        if position in self.tiles:
            return True
        else:
            return False

    def to_pixel(self, position, size=(0, 0), origin=(0, 0)):
        """Converts BoardPosition to pixel coordinates"""
        x = position[0] * self.tile_size + origin[0]
        y = position[1] * self.tile_size + origin[1]
        return board_position.Position(x, y)
    
    @property
    def container_width(self) -> int:
        """The width of the container"""
        return self.columns * self.tile_size

    @property
    def container_height(self) -> int:
        """The height of the container"""
        return self.rows * self.tile_size