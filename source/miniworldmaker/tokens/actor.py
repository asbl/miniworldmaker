from logging import *
from typing import Union
import pygame
import math
from miniworldmaker import tokens


class Actor(tokens.board_token.Token):
    log = getLogger("Actor")

    def __init__(self):
        """
        Initializes a new Actor
        """
        super().__init__()
        self.is_static = False

    def turn_left(self, degrees: int = 90) -> int:
        """
        Turns actor by *degrees* degrees left
        Args:
            degrees: degrees in left direction

        Returns: New direction

        """
        self.log.info("turn left {0} , {1}".format(self.direction, degrees))
        direction = self.direction + degrees
        self.direction = direction
        return self.direction

    def turn_right(self, degrees: int = 90):
        """
        Turns actor by *degrees* degrees right
        Args:
            degrees: degrees in left direction

        Returns: New direction

        """
        self.log.info("turn right {0} , {1}".format(self.direction, degrees))
        direction = self.direction - degrees
        self.direction = direction
        return self.direction

    def move(self, *, direction: Union[str, int] = "forward", distance: int = 1) -> tuple:
        """
        Moves actor *distance* steps into a *direction*.
        Args:
            direction: Direction in degrees (int) or a direction as string.
            distance: Number of steps to move

        Returns: New position

        """
        self.direction = self._value_to_direction(direction)
        destination = self.look(distance=distance, direction=direction)
        self.position = self.board.get_board_position_from_pixel(destination.topleft)
        if self.board:
            self.board.window.send_event_to_containers("actor_moved", self)
        self.log.info("Move to position {0}; Direction {1}".format(self.position, self.direction))
        return self.position

    def look(self, direction: Union[str, int] = "here", distance: int = 1, ) -> pygame.Rect:
        """
        Looks *distance* steps into a *direction*.
        Args:
            direction: The direction in degrees (int) or a direction as string
            distance: Number of steps to look

        Returns: Position

        """
        if direction == "here":
            self.board.window.send_event_to_containers("actor_looked", self.rect)
            return self.rect
        else:
            direction = self._value_to_direction(direction)
            x = self.position[0] + round(math.cos(math.radians(direction)) * distance)
            y = self.position[1] - round(math.sin(math.radians(direction)) * distance)
            return self.board.get_rect_from_board_position((x, y), self.rect)

    def is_looking_at_tokens(self, direction: Union[str, int] = "forward", distance: int = 1, actor_type=None):
        """
        Checks if actor is looking at actors
        Args:
            direction: Direction in degrees (int) or a direction as string.
            distance: Number of steps to move
            actor_type: Class name of actor types to look for. If actor_type == None, all actors are returned

        Returns: a list of all actors of given actor type

        """
        position = self.look(distance=distance, direction=direction)
        actors = self.board.get_tokens_in_area(position, actor_type)
        self.board.window.send_event_to_containers("actor_looked_at_tokens", (self, actors))
        return actors

    def is_looking_at_border(self, direction: Union[str, int] = "forward", distance: int = 1) -> list:
        """
        Checks if actor is looking at a border
        Args:
            direction: Direction in degrees (int) or a direction as string.
            distance: Number of steps to move

        Returns: a list of all borders ("top", "left", "right", "bottom") which are touched on given position.

        """
        position = self.look(distance=distance, direction=direction)
        borders = self.board.borders(position)
        self.board.window.send_event_to_containers("actor_is_looking_at_border", (self, borders))
        return borders

    def is_looking_on_board(self, direction: Union[str, int] = "forward", distance: int = 1) -> bool:
        """
        Checks if actor is looking at a position which is on the board
        Args:
            direction: Direction in degrees (int) or a direction as string.
            distance: Number of steps to move

        Returns: True if position is on board

        """
        position = self.look(distance=distance, direction=direction)
        on_board = self.board.on_board(position)
        self.board.window.send_event_to_containers("actor_is_looking_on_board", (self, on_board))
        return on_board

    def flip_x(self):
        """
        Flips the actor by 180° degrees

        """
        if not self._flip_x:
            self._flip_x = True
        else:
            self._flip_x = False
        self.turn_left(180)
