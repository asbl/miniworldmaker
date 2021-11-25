import math


class TokenBoardSensor():

    def __init__(self, token, board):
        super().__init__()
        self.token = token
        self.board = board

    def remove_from_board(self):
        """Removes a token from board
        """
        self.board.tokens.remove(self.token)
        self.token.board = None

    def point_towards_position(self, destination) -> float:
        """
        Token points towards a given position

        Args:
            destination: The position to which the actor should pointing

        Returns:
            The new direction

        """
        pos = self.token.center
        x = (destination[0] - pos[0])
        y = (destination[1] - pos[1])
        if x != 0:
            m = y / x
            if x < 0:
                # destination is left
                self.token.direction =  (math.degrees(math.atan(m)) - 90 )
            else:
                # destination is right
                self.token.direction = (math.degrees(math.atan(m)) + 90)
            return self.token.direction
        else:
            m = 0
            if destination[1] > self.token.position[1]:
                self.token.direction = 180
                return self.token.direction
            else:
                self.token.direction = 0
                return self.token.direction

    def remove(self):
        """
        Method is overwritten in subclasses
        """
        pass