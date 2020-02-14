import pygame
from miniworldmaker.app import app
from miniworldmaker.board_positions import board_position


class BoardRect(pygame.Rect):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = app.App.board

    def is_tile(self):
        if self.width == self.board.tile_size and self.height == self.board.tile_size:
            return True
        else:
            return False

    def borders(self):
        """
        Gets all borders the rect ist touching.

        Returns: A list of borders as strings: "left", "bottom", "right", or "top"

        """
        borders = []
        if self.topleft[0] <= 0:
            borders.append("left")
        if self.topleft[1] + self.height >= self.board.height:
            borders.append("bottom")
        if self.topleft[0] + self.width >= self.board.width:
            borders.append("right")
        if self.topleft[1] <= 0:
            borders.append("top")
        return borders

    def is_on_board(self):
        topleft_on_board = board_position.BoardPosition(self.left, self.top).is_on_board()
        bottom_right_on_board = board_position.BoardPosition(self.right, self .bottom).is_on_board()
        return topleft_on_board or bottom_right_on_board

    def colors(self, rect_borders = None):
            colors = []
            for x in range(self.width):
                if rect_borders is None or "left" in rect_borders:
                    color = self.board.background.color_at((self.x + x, self.y))
                    if color not in colors:
                        colors.append(color)
                if rect_borders is None or "right" in rect_borders:
                    color = self.board.background.color_at((self.x + x, self.y + self.height))
                    if color not in colors:
                        colors.append(color)
            for y in range(self.height):
                if rect_borders is None or "top" in rect_borders:
                    color = self.board.background.color_at((self.x, self.y + y))
                    if color not in colors:
                        colors.append(color)
                if rect_borders is None or "bottom" in rect_borders:
                    color = self.board.background.color_at((self.x + self.width, self.y + y))
                    if color not in colors:
                        colors.append(color)
            return colors
