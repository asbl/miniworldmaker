from miniworldmaker.boards import pixel_board
from miniworldmaker.connectors import physics_connector


class PhysicsBoard(pixel_board.PixelBoard):

    def add_to_board(self, token, position):
        """
        Adds a token to the board.
        The method is called with __init__ method of the token

        Args:
            token: The token to add to board.
            position: The position where the token should be added.

        Returns:

        """
        super().add_to_board(token, position)
        if not hasattr(token, "setup_physics"):
            @token.register
            def setup_physics(self):
                pass

    def _add_board_connector(self, token, position):
        token.board_connector = physics_connector.PhysicsBoardConnector(token, self)
        token.topleft = position[0], position[1]
