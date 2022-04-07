import miniworldmaker
from miniworldmaker.boards import hex_board
from miniworldmaker.boards.elements import hex_elements
from miniworldmaker.app import app
from miniworldmaker.appearances import hex_costume

class HexToken(miniworldmaker.Token):
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
        if position == None:
            position = (0, 0)
        super().__init__(position)
        self.costume = hex_costume.HexCostume(self)
        

    @classmethod
    def from_tile(cls, position):
        board = app.App.board
        tile = board.get_tile(position)
        position = tile.position
        return cls(position)

class HexBorder(miniworldmaker.Token):
    def __init__(self, position, border_direction):
        super().__init__(position)
        self.border_direction = border_direction
        self.costume = hex_costume.HexBorderCostume(self, border_direction)
