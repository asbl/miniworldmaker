import collections


class BoardPosition(collections.namedtuple('Point', ['x', 'y'])):
    """
    A BoardPosition Object represents a position on a Board.

    As a subclass of namedtuple, BoardPosition is for
    performance reasons not mutable. 

    On a tiled board, the BoardPosition does not describe pixels
    but tiles coordinates.
    """

    def __str__(self):
        return str("Pos(" + str(self.x) + "," + str(self.y) + ")")

    def up(self, value):
        """
        Gets the board position above the actual board-position

        Args:
            value: the number of fields above the actual position

        Returns:
            A new BoardPosition

        """
        return BoardPosition(self.x, self.y - value)

    def down(self, value):
        """
        Gets the board position below the actual board-position

        Args:
            value: the number of fields below the actual position

        Returns:
            A new BoardPosition

        """
        return BoardPosition(self.x, self.y + value)

    def left(self, value):
        """
        Gets the board position left of the the actual board-position

        Args:
            value: the number of fields left of the the actual position

        Returns:
            A new BoardPosition

        """
        return BoardPosition(self.x - value, self.y)

    def right(self, value):
        """
        Gets the board position right of the actual board-position

        Args:
            value: the number of fields right of the actual position

        Returns:
            A new BoardPosition

        """
        return BoardPosition(self.x + value, self.y - value)

    def add(self, x, y):
        """
        Adds x and y to the board positions x and y coordinate

        Returns: The new BoardPosition

        """
        return BoardPosition(self.x + x, self.y + y)

    def to_int(self):
        return (int(self.x), int(self.y))