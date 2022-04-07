from miniworldmaker.board_positions import board_position
from miniworldmaker.board_positions import board_rect_factory
import pygame


class BoardPositionHandler:
    def __init__(self, board):
        self.board = board
        self._mouse_position = None
        self._prev_mouse_position = None

    def update_positions(self):
        self._prev_mouse_position = self._mouse_position
        self._mouse_position = self.get_mouse_position()

    def get_mouse_position(self):
        pos = pygame.mouse.get_pos()
        clicked_container = self.board.app.container_manager.get_container_by_pixel(pos[0], pos[1])
        if clicked_container == self.board:
            return self.board.get_from_pixel(pos)
        else:
            return None

    @property
    def mouse_position(self):
        return self._mouse_position

    @property
    def prev_mouse_position(self):
        return self._prev_mouse_position

    def get_color(self, position):
        """
        Returns the board-color at the current board-position

        Returns: The board-color at the current board position as tuple
        with r,g,b value and transparency (e.g. (255, 0, 0, 100)

        """
        position = self._position_factory.create(position)
        if self.is_position_on_board(position):
            return self.board.background.get_color_from_pixel(position)
        else:
            return ()

    def near(self, pos1, pos2, distance):
        """
        Checks if two Board-Positions are near each other

        Args:
            other: A second Board-Position.
            distance: The size of the environment in which 2 positions are called "near".

        Returns:
            True, If the Positions are near each other.

        """
        pos1 = board_position.Position.create(pos1)
        pos2 = board_position.Position.create(pos2)
        if (
            pos1.x <= pos2.x + distance
            and pos1.x >= pos2.x - distance
            and pos1.y <= pos2.y + distance
            and pos1.y >= pos2.y - distance
        ):
            return True
        else:
            return False

    def is_position_on_board(self, pos):
        """
        Checks if Position is on board

        Returns:
            True, if Position is on board.
        """
        if pos.x >= 0 and pos.y >= 0 and pos.x < self.board.columns and pos.y < self.board.rows:
            return True
        else:
            return False

    def get_borders_from_rect(self, rect):
        """
        Gets all borders the rect ist touching.

        Returns: A list of borders as strings: "left", "bottom", "right", or "top"

        """
        rect = board_rect_factory.BoardRectFactory(self.board).create(rect)
        borders = []
        if rect.topleft[0] <= 0:
            borders.append("left")
        if rect.topleft[1] + rect.height >= self.board.height:
            borders.append("bottom")
        if rect.topleft[0] + rect.width >= self.board.width:
            borders.append("right")
        if rect.topleft[1] <= 0:
            borders.append("top")
        return borders

    def is_rect_completly_on_board(self, rect):
        rect = board_rect_factory.BoardRectFactory(self.board).create(rect)
        topleft_on_board = self.is_position_on_board(
            board_rect_factory.BoardRectFactory(self.board).create(tuple([rect.left, rect.top]))
        )
        bottom_right_on_board = self.is_position_on_board(
            board_rect_factory.BoardRectFactory(self.board).create(tuple([rect.right, rect.bottom]))
        )
        return topleft_on_board or bottom_right_on_board

    def get_colors_in_rect(self, rect, rect_borders=None):
        colors = []
        rect = board_rect_factory.BoardRectFactory.create(rect)
        for x in range(self.width):
            if rect_borders is None or "left" in rect_borders:
                color = self.board.background.get_color_from_pixel((rect.x + x, rect.y))
                if color not in colors:
                    colors.append(color)
            if rect_borders is None or "right" in rect_borders:
                color = self.board.background.get_color_from_pixel((rect.x + x, rect.y + rect.height))
                if color not in colors:
                    colors.append(color)
        for y in range(self.height):
            if rect_borders is None or "top" in rect_borders:
                color = self.board.background.get_color_from_pixel((rect.x, rect.y + y))
                if color not in colors:
                    colors.append(color)
            if rect_borders is None or "bottom" in rect_borders:
                color = self.board.background.get_color_from_pixel((rect.x + rect.width, rect.y + y))
                if color not in colors:
                    colors.append(color)
        return colors
