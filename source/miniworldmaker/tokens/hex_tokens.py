import miniworldmaker

import sys
from miniworldmaker import conf

sys.path.append(conf.ROOT_DIR)

from boards import hex_board
from boards.elements import hex_elements
from app import app
from appearances import hex_costume
from tokens import token

class HexToken(token.Token):
    """Shape is the parent class for various geometric objects that can be created.

    Each geometric object has the following properties:

    * border: The border thickness of the object.
    * is_filled: True/False if the object should be filled.
    * fill_color: The fill color of the object
    * border_color: The border color of the object.

    .. image:: ../_images/shapes.png
        :width: 60%
        :alt: Shapes
    """

    def __init__(self, position: hex_elements.CubeCoord = None):
        super().__init__(position)
        self.costume = hex_costume.HexCostume(self)
        

    @classmethod
    def from_tile(cls, position):
        board = app.App.board
        tile = board.get_tile(position)
        position = tile.position
        return cls(position)


class HexEdgeToken(token.Token):
    def __init__(self, position : hex_elements.CubeCoord):
        super().__init__(position)
        self.position = position
        self.costume = hex_costume.HexEdgeCostume(self)

    @classmethod
    def from_tile(cls, position, direction):
        edge = hex_elements.HexEdge(position, direction)
        edge_tkn = HexEdgeToken(edge.position)
        assert edge_tkn.board.get_edge(edge.direction) == edge
