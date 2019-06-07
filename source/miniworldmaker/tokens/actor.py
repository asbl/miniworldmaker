import math
from logging import *
from typing import Union

import pygame
from miniworldmaker.boards import board_position
import miniworldmaker.tokens.board_token as token


class Actor(token.Token):

    log = getLogger("Actor")

    def __init__(self, position = None):
        """ Initializes a new actor

        Args:
            position: The position on the board as tuple. If None, the actor will not be placed on the board.
        """
        super().__init__(position)
        self.is_static = False
        self.costume.is_rotatable = True
        self.registered_events.extend(["key_pressed", "key_down"])
        self._orientation = 0

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

    def point_towards_position(self, destination, center = False) -> int:
        """
        Actor points towards a given position

        Args:
            destination: The position to which the actor should pointing

        Returns:
            The new direction

        """
        if center is True:
            pos = self.rect.center
        else:
            pos = self.position
        x =  (destination[0] - pos[0])
        y =  (destination[1] - pos[1])
        if x != 0:
            m = y / x
        else:
            m = 0
            if destination[1] > self.position[1]:
                self.direction = 180
                return 180
            else:
                self.direction = 0
                return 0
        if destination[0] > self.position[0]:
            self.direction = 90 + math.degrees(math.atan(m))
        else:
            self.direction = 270 +  math.degrees(math.atan(m))
        return self.direction

    def point_towards_token(self, token) -> int:
        """
        Actor points towards a given position

        Args:
            destination_position: The position to which the actor should pointing

        Returns:
            The new direction

        """
        pos = token.rect.center
        return self.point_towards_position(pos, center = True)

    def turn_left(self, degrees: int = 90) -> int:
        """Turns actor by *degrees* degrees left

        Args:
            degrees: degrees in left direction

        Returns:
            New direction

        """
        self.direction = self.direction - degrees
        return self.direction

    def turn_right(self, degrees: int = 90):
        """Turns actor by *degrees* degrees right

        Args:
            degrees: degrees in left direction

        Returns:
            New direction

        """
        self.direction = self.direction + degrees
        return self.direction

    def move_in_direction(self, direction : Union[int, str]):
        """Moves actor *distance* steps into a *direction*.

        Args:
            distance: Number of steps to move

        Returns:
            The actor

        """
        direction = direction = self._value_to_direction(direction)
        self.direction = direction
        self.costume.is_rotatable = False
        self.move()
        return self

    def move_to(self, position : board_position.BoardPosition):
        """Moves actor *distance* steps into a *direction*.

        Args:
            position: The position to which the actor should move

        Returns:
            The actor

        """
        self.position = position
        return self

    def move(self, distance: int = 0):
        """Moves actor *distance* steps into a *direction*.

        Args:
            distance: Number of steps to move. If distance = 0, the actor speed will be used.

        Returns:
            The actor

        """
        if distance == 0:
            distance = self.speed
        destination = self.look(direction = self.direction, distance=distance)
        self.position = self.board.get_board_position_from_pixel(destination.topleft)
        self.last_direction=self.direction
        return self

    def look(self, direction: int = -9999, distance: int = 1, style="rect") -> Union[list, pygame.Surface]:
        """Looks *distance* steps into a *direction*.

        Args:
            distance: Number of steps to look

        Returns:
            A destination Surface
        """
        if direction == -9999:
            direction = self.direction
        if style == "rect":
            return self.get_destination(direction, distance)
        elif style == "line":
            return self.get_line(direction, distance)

    def get_destination(self, direction, distance):
        x = self.position[0] + round( math.sin(math.radians(direction)) * distance)
        y = self.position[1] - round(math.cos(math.radians(direction)) * distance)
        return board_position.BoardPosition((x, y)).to_surface(rect=self.rect)

    def get_line(self, direction, distance):
        line = []
        i = 0
        while i < distance:
            print(direction,math.sin(math.radians(direction)),math.cos(math.radians(direction)))
            position = self.rect.center
            x = position[0] + round(math.sin(math.radians(direction)) * i)
            y = position[1] - round(math.cos(math.radians(direction)) * i)
            pos = board_position.BoardPosition((x, y))
            if not self.rect.collidepoint(pos[0], pos[1]):
                line.append(pos)
            else:
                distance += 1
            i += 1
        return line

    def delta_x(self, distance):
        return round( math.sin(math.radians(self.direction)) * distance)

    def delta_y(self, distance):
        return - round(math.cos(math.radians(self.direction)) * distance)

    def bounce_from_border(self, borders):
        """ Bounces the actor from a border.

        Args:
            borders: A list of borders as strings e.g. ["left", "right"]

        Returns: The actor

        """
        angle = self.direction
        if ("top" in borders and ((self.direction <= 0 and self.direction > -90 or self.direction <= 90 and self.direction>=0))):
            self.point_in_direction(0)
            incidence = self.direction - angle
            self.turn_left(180 - incidence)
        elif ("bottom" in borders and ((self.direction < -90 and self.direction >= -180) or (self.direction > 90 and self.direction <= 180))):
            self.point_in_direction(180)
            incidence = self.direction - angle
            self.turn_left(180 - incidence)
        elif ("left" in borders and self.direction <= 0):
            self.point_in_direction(-90)
            incidence = self.direction - angle
            self.turn_left(180 - incidence)
        elif ("right" in borders and (self.direction >= 0)):
            self.point_in_direction(90)
            incidence = self.direction - angle
            self.turn_left(180 - incidence)
        else:
            pass
        return self

    def bounce_from_token(self, token):
        """experimental: Bounces actor from another token
        Args:
            token: the token

        Returns: the actor

        """
        angle = self.direction
        self.move(-self.speed)
        self.point_towards_token(token)
        incidence = self.direction - angle
        self.turn_left(180 - incidence)
        return self

    def sensing_tokens(self, distance: int = -1, token=None, exact = False) -> list:
        """Checks if Actor is sensing Tokens in front

        Args:
            distance: Number of steps to look for tokens  (0: at actor position)
            token: Class name of token types to look for. If token == None, all token are returned
            exact: If exact is True, then collision handling will be done with masks (slower, more precise) instead of rectangles

        Returns:
            a list of tokens

        """
        if distance < 0:
            distance = self.speed
        destination_rect = self.look(distance=distance)
        tokens = self.board.get_tokens_in_area(destination_rect, token, exclude=self)
        if exact:
            return  [token for token in tokens if pygame.sprite.collide_mask(self,token)]
        return tokens

    def sensing_token(self, distance: int = -1, token=None, exact = False) -> Union[token.Token,None]:
        """Checks if actor is sensing a single token in front. See sensing_tokens

        Args:
            distance: Number of steps to look for tokens  (0: at actor position)
            token: Class name of token types to look for. If token == None, all token are returned
            exact: If exact is True, then collision handling will be done with masks (slower, more precise) instead of rectangles

        Returns:
            A single token

        """
        if distance < 0:
            distance = self.speed
        destination_rect = self.look(distance=distance)
        token = self.board.get_token(destination_rect, token, exclude=self)
        if exact and token is not None:
            if not pygame.sprite.collide_mask(self, token):
                tokens = self.sensing_tokens(exact= True, token = token)
                if tokens:
                    return tokens[0]
                else:
                    return None
        return token

    def sensing_borders(self, distance: Union[int, None] = None) -> list:
        """Checks if actor is sensing a border in front

        Args:
            distance: Number of steps to look for borders  (0: at actor position)

        Returns:
            a list of all borders ("top", "left", "right", "bottom") which are sensed on given position.

        """
        if distance is None:
            distance = self.speed
        destination_rect = self.look(distance=distance)
        borders = self.board.borders(destination_rect)
        self.board.window.send_event_to_containers("actor_is_looking_at_border", self)
        return borders

    def sensing_on_board(self, distance:Union[int, None] = None) -> bool:
        """Checks if actor is sensing a position inside the board

        Args:
            distance: Number of steps to look for

        Returns:
            True if position is on board

        """
        if distance is None:
            distance = self.speed
        position = self.look(direction = self.direction, distance=distance)
        on_board = self.board.is_on_board(position)
        return on_board

    def sensing_color(self,  color, distance:Union[int, None] = None,) -> int:
        """Sensing the number of pixels of a given color

        Args:
            distance: Number of steps to look for color
            color: The color to look for

        Returns:
            The number of pixels filled with the given color. If no color ist given, the
            color found in the center of actor rectangle will be returned.

        """
        if distance is None:
            distance = self.speed
        destination_rect = self.look(distance=distance)
        colors = self.board.find_colors(destination_rect, color)
        return colors

    def sensing_colors(self, distance:Union[int, None] = None) -> set:
        """ Gets all colors the actor is sensing

        Args:
            distance: Number of steps to look for color

        Returns:
            All colors the actor is sensing as set

        """
        if distance is None:
            distance = self.speed
        direction = self.direction
        line = self.look(distance=distance, direction = direction, style = "line")
        colors = self.board.get_colors_at_line(line)
        return colors

    def flip_x(self) -> int:
        """Flips the actor by 180° degrees

        """
        if not self.costume.is_flipped:
            self.costume.is_flipped = True
        else:
            self.costume.is_flipped = False
        self.turn_left(180)
        return self.direction

    def __str__(self):
        str = super().__str__()
        if self.board:
            str = str + "\n  * Direction: {0}".format(self.direction)
        return str