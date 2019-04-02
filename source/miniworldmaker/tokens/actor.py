from logging import *
from typing import Union
import pygame
import math
from miniworldmaker import tokens
from boards import board_position
from tokens import token


class Actor(tokens.token.Token):
    log = getLogger("Actor")

    def __init__(self):
        """Initializes a new Actor
        """
        super().__init__()
        self.is_static = False

    def point_in_direction(self, direction) -> int:
        """
        Actor points in given direction

        Args:
            direction: Direction the actor should point to

        Returns:
            The new direction as integer

        """
        direction = direction = self._value_to_direction(direction)
        self.direction = direction
        return self.direction

    def point_towards_position(self, board_position) -> int:
        """
        Actor points towards a given position

        Args:
            board_position: The position to which the actor should pointing

        Returns:
            The new direction

        """
        x = board_position[0] - self.position[0]
        y = - (board_position[1] - self.position[1])
        if x != 0:
            m = y / x
        else:
            m = 0
        self.direction = math.degrees(math.tan(m))
        return self.direction

    def turn_left(self, degrees: int = 90) -> int:
        """Turns actor by *degrees* degrees left

        Args:
            degrees: degrees in left direction

        Returns:
            New direction

        """
        direction = self.direction + degrees
        self.direction = direction
        return self.direction

    def turn_right(self, degrees: int = 90):
        """Turns actor by *degrees* degrees right

        Args:
            degrees: degrees in left direction

        Returns:
            New direction

        """
        direction = self.direction - degrees
        self.direction = direction
        return self.direction

    def move(self, distance: int = 1) -> board_position.BoardPosition:
        """Moves actor *distance* steps into a *direction*.

        Args:
            distance: Number of steps to move

        Returns:
            New position

        """
        destination = self.look(distance=distance, direction="forward")
        self.position = self.board.get_board_position_from_pixel(destination.topleft)
        if self.board:
            self.board.window.send_event_to_containers("actor_moved", self)
        return self.position

    def look(self, direction: Union[str, int] = "here", distance: int = 1, ) -> pygame.Rect:
        """Looks *distance* steps into a *direction*.

        Args:
            direction: The direction in degrees (int) or a direction as string
            distance: Number of steps to look

        Returns:
            A destination Rectangle
        """
        if direction == "here":
            return self.rect
        else:
            direction = self._value_to_direction(direction)
            x = self.position[0] + round(math.cos(math.radians(direction)) * distance * self.board.steps)
            y = self.position[1] - round(math.sin(math.radians(direction)) * distance * self.board.steps)
            return board_position.BoardPosition(x, y).to_rect(rect=self.rect)

    def sensing_tokens(self, distance: int = 1, token=None):
        """Checks if Actor is sensing Tokens in front

        Args:
            distance: Number of steps to look for tokens  (0: at actor position)
            token: Class name of token types to look for. If token == None, all token are returned


        Returns:
            a list of tokens

        """
        destination_rect = self.look(distance=distance, direction="forward")
        tokens = self.board.get_tokens_in_area(destination_rect, token, exclude=self)
        return tokens

    def sensing_token(self, distance: int = 1, token=None) -> token.Token:
        """Checks if actor is sensing a single token in front. See sensing_tokens

        Args:
            distance: Number of steps to look for tokens  (0: at actor position)
            token: Class name of token types to look for. If token == None, all token are returned

        Returns:
            A single token

        """
        destination_rect = self.look(distance=distance, direction="forward", )
        token = self.board.get_token_in_area(destination_rect, token, exclude=self)
        return token

    def sensing_borders(self, direction: Union[str, int] = "forward", distance: int = 1) -> list:
        """Checks if actor is sensing a border in front

        Args:
            distance: Number of steps to look for borders  (0: at actor position)

        Returns:
            a list of all borders ("top", "left", "right", "bottom") which are sensed on given position.

        """
        destination_rect = self.look(distance=distance, direction=direction)
        borders = self.board.borders(destination_rect)
        self.board.window.send_event_to_containers("actor_is_looking_at_border", (self, borders))
        return borders

    def sensing_on_board(self, distance: int = 1) -> bool:
        """Checks if actor is sensing a position inside the board

        Args:
            distance: Number of steps to look for

        Returns:
            True if position is on board

        """
        position = self.look(distance=distance, direction="forward")
        on_board = self.board.is_on_board(position)
        return on_board

    def sensing_color(self, distance: int = 1) -> list:
        """Checks the color of board under the actor

        Args:
            distance: Number of steps to look for a color

        Returns:
            The color found in the center of the rectangle of the actor.

        """
        destination_rect = self.look(distance=distance, direction=direction)
        color = self.board.get_color_at_board_position(destination_rect.center)
        return color

    def is_sensing_color(self, color, distance: int = 1) -> int:
        """Checks if actor is sensing a color

        Args:
            distance: Number of steps to look for color

        Returns:
            The number of pixels filled with the given color

        """
        destination_rect = self.look(distance=distance, direction="forward")
        colors = self.board.find_colors(destination_rect, color)
        return colors


    def flip_x(self):
        """Flips the actor by 180° degrees

        """
        if not self._flip_x:
            self._flip_x = True
        else:
            self._flip_x = False
        self.turn_left(180)
