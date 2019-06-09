from miniworldmaker.boards.board import Board
from miniworldmaker.tokens.board_token import Token
from typing import Union


class PixelBoard(Board):

    def __init__(self, columns=40, rows=40):
        super().__init__(columns=columns, rows=rows)
        self.default_actor_speed = 3

    def add_to_board(self, token: Token, position) -> Token:
        super().add_to_board(token, position)
        if token.size == (0, 0):
            token.size = (30, 30)
        return token

    def remove_from_board(self, token: Token):
        token_id = token.token_id
        super().remove_from_board(token)

    def borders(self, rect):
        borders = []
        if rect.topleft[0] <= 0:
            borders.append("left")
        if rect.topleft[1] + rect.height >= self.height:
            borders.append("bottom")
        if rect.topleft[0] + rect.width >= self.width:
            borders.append("right")
        if rect.topleft[1] <= 0:
            borders.append("top")
        return borders

    def get_touching_borders(self, rect) -> list:
        borders = []
        if rect.topleft[0] <= 0:
            borders.append("left")
        if rect.topleft[1] + rect.height >= self.height:
            borders.append("bottom")
        if rect.topleft[0] + rect.width >= self.width:
            borders.append("right")
        if rect.topleft[1] <= 0:
            borders.append("top")
        return borders

    def update(self):
        super().update()
