import math
from typing import Union

import miniworldmaker.tokens.token as tkn
import pygame
from miniworldmaker.boards import board_position
from miniworldmaker.boards import board_position as bp


class Actor(tkn.Token):
    """ Initializes a new actor

    Args:
        position: The position on the board as tuple.
        If None, the actor will not be placed on the board.

    Examples:

        Usually you create your own subclass of Actor:

        >>> class Player(Actor):
        >>>     def __init__(self, position):
        >>>     super().__init__(position)
        >>>
        >>>
        >>> class MyBoard(PixelBoard):
        >>>     def __init__(self):
        >>>     self.player = Player(position = (100,60))
    """

    def __init__(self, position = None):

        super().__init__(position)
        self.is_static = False
        self.costume.is_rotatable = True
        self._orientation = 0
        self.registered_event_handlers["mouse_left"] = self.on_mouse_left
        self.registered_event_handlers["mouse_right"] = self.on_mouse_left
        self.registered_event_handlers["mouse_motion"] = self.on_mouse_motion
        self.registered_event_handlers["key_pressed"] = self.on_key_pressed
        self.registered_event_handlers["key_down"] = self.on_key_down
        self.registered_event_handlers["key_up"] = self.on_key_up
        self.on_setup()

    def add_to_board(self, board, position: board_position.BoardPosition):
        super().add_to_board(board, position)
        from miniworldmaker.boards import pixel_board as pb
        from miniworldmaker.boards import tiled_board as tb
        if issubclass(self.board.__class__, pb.PixelBoard):
            cls = self.__class__
            self.__class__ = cls.__class__(cls.__name__ , (cls, PixelBoardActor), {})
        elif issubclass(self.board.__class__, tb.TiledBoard):
            cls = self.__class__
            self.__class__ = cls.__class__(cls.__name__ , (cls, TiledBoardActor), {})


    def on_key_pressed(self, keys):
        pass

    def on_key_up(self, keys):
        pass

    def on_key_down(self, keys):
        pass

    def on_mouse_left(self, mouse_pos):
        pass

    def on_mouse_right(self, mouse_pos):
        pass

    def on_mouse_motion(self, mouse_pos):
        pass

    def on_setup(self):
        pass

    def move_in_direction(self, direction : Union[int, str]):
        """Moves actor *distance* steps into a *direction*.

        Args:
            direction: Direction as angle

        Returns:
            The actor

        """
        direction = self._value_to_direction(direction)
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
        """Moves actor *distance* steps.

        Args:
            distance: Number of steps to move.
            If distance = 0, the actor speed will be used.

        Returns:
            The actor

        Examples:

            >>> class Robot(Actor):
            >>>    def act(self):
            >>>         if self.sensing_on_board():
            >>>             self.move()
        """
        if distance == 0:
            distance = self.speed
        destination = self.get_destination(self.direction, distance)
        self.last_position = self.position
        self.position = destination
        self.last_direction=self.direction
        return self

    def move_back(self):
        self.position = self.last_position
        self.direction = self.last_direction

    def get_destination(self, direction, distance) -> bp.BoardPosition:
        x = self.position[0] + round(math.sin(math.radians(direction)) * distance)
        y = self.position[1] - round(math.cos(math.radians(direction)) * distance)
        return board_position.BoardPosition(x, y)

    def look(self, distance: int = 1, direction: int = -9999, style="rect") -> Union[list, pygame.Surface]:
        """Looks *distance* steps into a *direction*.

        Args:
            distance: Number of steps to look
            direction: The direction to look

        Returns:
            A destination Surface
        """
        if direction == -9999:
            direction = self.direction
        if style == "rect":
            return self.get_destination(direction, distance)
        elif style == "line":
            return self.get_line(direction, distance)

    def get_line(self, direction, distance):
        line = []
        i = 0
        while i < distance:
            position = self.rect.center
            x = position[0] + round(math.sin(math.radians(direction)) * i)
            y = position[1] - round(math.cos(math.radians(direction)) * i)
            pos = board_position.BoardPosition(x, y)
            if not self.rect.collidepoint(pos[0], pos[1]):
                line.append(pos)
            else:
                distance += 1
            i += 1
        return line

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

    def sensing_tokens(self, distance: int = -1, token_type=None, exact = False) -> list:
        """Checks if Actor is sensing Tokens in front

        Args:
            distance: Number of steps to look for tokens  (0: at actor position)
            token_type: Class name of token types to look for. If token == None, all token are returned
            exact: If exact is True, then collision handling will be done with masks (slower, more precise) instead of rectangles

        Returns:
            a list of tokens

        """
        pass

    def sensing_token(self, distance: int = -1, token_type=None, exact = False) -> Union[tkn.Token, None]:
        """Checks if actor is sensing a single token in front. See sensing_tokens

        Args:
            distance: Number of steps to look for tokens  (0: at actor position)
            token_type: Class name of token types to look for. If token == None, all token are returned
            exact: If exact is True, then collision handling will be done with masks (slower, more precise) instead of rectangles

        Returns:
            A single token

        """
        pass

    def sensing_borders(self, distance: int = 1, ) -> list:
        """Checks if actor is sensing a border in front

        Args:
            distance: Number of steps to look for borders  (0: at actor position)

        Returns:
            a list of all borders ("top", "left", "right", "bottom") which are sensed on given position.

        """
        pass

    def sensing_on_board(self = None, distance = 0) -> bool:
        """Checks if actor is sensing a position inside the board

        Args:
            distance: Number of steps to look for

        Returns:
            True if position is on board

        """
        pass

    def sensing_colors(self, distance:Union[int, None] = None, colors: Union[tuple, list]=[]) -> set:
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
        colorlist = self.board.get_colors_at_line(line)
        if type(colors) == tuple:
            colors = [colors]
        if not colors:
            return colorlist
        intersections = [value for value in colorlist if value in colors]
        return intersections

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
            str = str + " with Direction: {0}".format(self.direction)
        return str

class PixelBoardActor(Actor):

    def get_target_rect(self, distance):
        target = self.get_destination(self.direction, distance)
        return target.to_rect(self.rect)

    @staticmethod
    def filter_actor_list(a_list, actor_type):
        return [actor for actor in a_list if type(actor) == actor_type]

    def sensing_on_board(self = None, distance = 0) -> bool:
        """Checks if actor is sensing a position inside the board

        Args:
            distance: Number of steps to look for

        Returns:
            True if position is on board

        """
        target_rect = self.get_target_rect(distance)
        topleft_on_board = board_position.BoardPosition(target_rect.left, target_rect.top).is_on_board()
        bottom_right_on_board = board_position.BoardPosition(target_rect.right, target_rect.bottom).is_on_board()
        return topleft_on_board and bottom_right_on_board

    def sensing_borders(self, distance: int = 1, ) -> list:
        """Checks if actor is sensing a border in front

        Args:
            distance: Number of steps to look for borders  (0: at actor position)

        Returns:
            a list of all borders ("top", "left", "right", "bottom") which are sensed on given position.

        """

        for i in range(distance + 1):
            target_rect = self.get_target_rect(distance)
            borders = self.board.borders(target_rect)
            if borders:
                self.board.window.send_event_to_containers("actor_is_looking_at_border", self)
                return borders
        else:
            return []

    def sensing_tokens(self, distance: int = 1, token_type=None, exact = False) -> list:
        """Checks if Actor is sensing Tokens in front

        Args:
            distance: Number of steps to look for tokens  (0: at actor position)
            token_type: Class name of token types to look for. If token == None, all token are returned
            exact: If exact is True, then collision handling will be done with masks (slower, more precise) instead of rectangles

        Returns:
            a list of tokens

        """
        pass

    def sensing_token(self, distance: int = 1, token_type=None, exact = False) -> Union[tkn.Token, None]:
        """Checks if actor is sensing a single token in front. See sensing_tokens

        Args:
            distance: Number of steps to look for tokens  (0: at actor position)
            token_type: Class name of token types to look for. If token == None, all token are returned
            exact: If exact is True, then collision handling will be done with masks (slower, more precise) instead of rectangles

        Returns:
            A single token

        """
        destination_rect = self.get_target_rect(distance)
        token = self.board.get_tokens_in_area(destination_rect, singleitem= True, exclude= self, token_type = token_type)
        if exact and token:
            if pygame.sprite.collide_mask(self, token):
                return token
            else:
                return None
        return None


class TiledBoardActor(Actor):

    def sensing_on_board(self = None, distance = 0) -> bool:
        """Checks if actor is sensing a position inside the board

        Args:
            distance: Number of steps to look for

        Returns:
            True if position is on board

        """
        target = self.get_destination(self.direction, distance)
        on_board = target.is_on_board()
        return on_board

    def sensing_tokens(self, distance: int = 1, token_type=None, exact = False) -> list:
        """Checks if Actor is sensing Tokens in front

        Args:
            distance: Number of steps to look for tokens  (0: at actor position)
            token_type: Class name of token types to look for. If token == None, all token are returned
            exact: If exact is True, then collision handling will be done with masks (slower, more precise) instead of rectangles

        Returns:
            a list of tokens

        """
        target = self.get_destination(self.direction, distance)
        return self.board.get_tokens_at_position(target, token_type, exclude = self)

    def sensing_token(self, distance: int = 1, token_type=None, exact = False) -> list:
        """Checks if Actor is sensing Tokens in front

        Args:
            distance: Number of steps to look for tokens  (0: at actor position)
            token_type: Class name of token types to look for. If token == None, all token are returned
            exact: If exact is True, then collision handling will be done with masks (slower, more precise) instead of rectangles

        Returns:
            a list of tokens

        """
        target = self.get_destination(self.direction, distance)
        return self.board.get_tokens_at_position(target, token_type, exclude = self, singleitem = True)
