from logging import *
from typing import Union
import pygame
import math
from miniworldmaker.tokens import token
from miniworldmaker.boards import board_position


class Actor(token.Token):
    log = getLogger("Actor")

    def __init__(self, position = None):
        """Initializes a new Actor
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

    def point_towards_position(self, destination_position, center = False) -> int:
        """
        Actor points towards a given position

        Args:
            destination_position: The position to which the actor should pointing

        Returns:
            The new direction

        """
        if center is True:
            pos = self.rect.center
        else:
            pos = self.position
        x =  (destination_position[0] - pos[0])
        y =  (destination_position[1] - pos[1])
        if x != 0:
            m = y / x
        else:
            m = 0
            if destination_position[1] > self.position[1]:
                self.direction = 180
                return 180
            else:
                self.direction = 0
                return 0
        if destination_position[0] > self.position[0]:
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
        destination = self.look(distance=distance)
        self.position = self.board.get_board_position_from_pixel(destination.topleft)
        self.last_direction=self.direction
        return self

    def look(self, distance: int) -> pygame.Rect:
        """Looks *distance* steps into a *direction*.

        Args:
            distance: Number of steps to look

        Returns:
            A destination Rectangle
        """
        x = self.position[0] + self.delta_x(distance)
        y = self.position[1] + self.delta_y(distance)
        return board_position.BoardPosition(x, y).to_rect(rect=self.rect)

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
        elif ("bottom" in borders and ((self.direction < -90 and self.direction > -180) or (self.direction > 90 and self.direction < 180))):
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
        token = self.board.get_token_in_area(destination_rect, token, exclude=self)
        if exact and token is not None:
            if not pygame.sprite.collide_mask(self, token):
                tokens = self.sensing_tokens(exact= True, token = token)
                if tokens:
                    return tokens[0]
                else:
                    return None
        return token

    def sensing_borders(self, distance: int = -1) -> list:
        """Checks if actor is sensing a border in front

        Args:
            distance: Number of steps to look for borders  (0: at actor position)

        Returns:
            a list of all borders ("top", "left", "right", "bottom") which are sensed on given position.

        """
        if distance < 0:
            distance = self.speed
        destination_rect = self.look(distance=distance)
        borders = self.board.borders(destination_rect)
        self.board.window.send_event_to_containers("actor_is_looking_at_border", (self, borders))
        return borders

    def sensing_on_board(self, distance: int = -1) -> bool:
        """Checks if actor is sensing a position inside the board

        Args:
            distance: Number of steps to look for

        Returns:
            True if position is on board

        """
        if distance < 0:
            distance = self.speed
        position = self.look(distance=distance)
        on_board = self.board.is_on_board(position)
        return on_board

    def sensing_color(self, color = None, distance: int = -1) -> Union[int, list]:
        """Checks if actor is sensing a color

        Args:
            distance: Number of steps to look for color
            color: The color to look for

        Returns:
            The number of pixels filled with the given color. If no color ist given, the
            color found in the center of actor rectangle will be returned.

        """
        if distance < 0:
            distance = self.speed
        destination_rect = self.look(distance=distance)
        if color == None:
            return self.board.get_color_at_board_position(destination_rect.center)
        colors = self.board.find_colors(destination_rect, color)
        return colors

    def flip_x(self):
        """Flips the actor by 180° degrees

        """
        if not self.costume.is_flipped:
            self.costume.is_flipped = True
        else:
            self.costume.is_flipped = False
        self.turn_left(180)

