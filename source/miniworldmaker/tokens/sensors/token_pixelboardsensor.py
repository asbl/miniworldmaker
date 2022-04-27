import math
from typing import Union, Optional

import pygame

import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.board_positions.board_rect as board_rect
import miniworldmaker.tokens.sensors.token_boardsensor as boardsensor
import miniworldmaker.tokens.token as token_mod
import miniworldmaker.boards.board as board_mod


class TokenPixelBoardSensor(boardsensor.TokenBoardSensor):
    """Sensor for Tokens on PixelBoard.
    """

    def __init__(self, token: "token_mod.Token", board: "board_mod.Board"):
        super().__init__(token, board)

    def sensing_on_board(self, distance: int = 0) -> bool:
        target_rect = self.get_destination_rect(distance)
        return self.is_rect_completly_on_board(target_rect)

    def sensing_borders(self, distance: int = 0) -> list:
        """
        The function compares the rectangle (or alternatively the
        path that the rectangle of the object **distance** pixels travels)
        with the edges of the playing field.
        """
        for _ in range(distance + 1):
            target_rect = self.get_destination_rect(distance)
            borders = self.get_borders_from_rect(target_rect)
            if borders:
                return borders
            else:
                return []

    def sensing_colors(self, colors: Union[tuple, list] = (), distance: int = 0) -> list:
        if type(colors) == tuple:
            colors = [colors]
        line = self.get_line_in_direction(self.token.center, self.token.direction, distance)
        colorlist = self.board.get_colors_at_line(line)
        if not colors:
            return colorlist
        intersections = [value for value in colorlist if value in colors]
        return intersections

    def get_destination_rect(self, distance: int) -> "board_rect.Rect":
        destination_pos = self.get_destination(self.token.position, self.token.direction, distance)
        destination_pos = board_position.Position.create(destination_pos)
        rect = board_rect.Rect.from_position(destination_pos, dimensions=self.token.size)
        return rect

    def get_line_in_direction(self, start, direction: Union[int, float], distance: int):
        return [self.get_destination(start, direction, i) for i in range(distance)]

    def get_line_to(self, start, target):
        sampling_rate = int(math.sqrt((target[0] - start[0]) ** 2 + target[1] - start[1] ** 2))
        x_spacing = (target[0] - start[0]) / (sampling_rate + 1)
        y_spacing = (target[1] - start[1]) / (sampling_rate + 1)
        return [board_position.Position.create((start[0] + i * x_spacing, start[1] + i * y_spacing) for i in
                                               range(1, sampling_rate + 1))]

    @staticmethod
    def get_destination(start, direction, distance) -> "board_position.Position":
        exact_position_x = start[0] + math.sin(math.radians(direction)) * distance
        exact_position_y = start[1] - math.cos(math.radians(direction)) * distance
        pos = board_position.Position.create((exact_position_x, exact_position_y))
        return pos

    @staticmethod
    def filter_actor_list(a_list, actor_type):
        return [actor for actor in a_list if type(token_mod.Token) == actor_type]

    def sensing_tokens(self, token_filter=None, distance: int = 0, collision_type="default") -> list:
        destination_rect = self.get_destination_rect(distance=distance)
        tokens = self.get_tokens_at_rect(destination_rect)
        if collision_type == "default":
            collision_type = "mask"
        else:
            collision_type = self.token.collision_type
        if collision_type == "circle":
            tokenlist = [
                token for token in tokens if pygame.sprite.collide_circle(self.token, token)]
        elif collision_type == "rect" or collision_type == "static-rect":
            tokenlist = [
                token for token in tokens if pygame.sprite.collide_rect(self.token, token)]
        elif collision_type == "mask":
            tokenlist = [
                token for token in tokens if pygame.sprite.collide_mask(self.token, token)]
        tokenlist = self.remove_self_from_token_list(tokenlist)
        tokenlist = self.filter_token_list(tokenlist, token_filter)
        return tokenlist

    def sensing_token(self, token_filter=None, distance: int = 0) -> Union["token_mod.Token", None]:
        destination_rect = self.get_destination_rect(distance)
        tokens = [self.get_single_token_at_rect(destination_rect)]
        tokens = self.filter_token_list(tokens, token_filter)
        if self.token.collision_type == "default":
            collision_type = "mask"
        else:
            collision_type = self.token.collision_type
        if not tokens:
            return None
        for token in tokens:
            if collision_type == "circle" and pygame.sprite.collide_circle(self.token, token):
                return token
            if collision_type == "rect" or collision_type == "static-rect" and pygame.sprite.collide_rect(self.token,
                                                                                                          token):
                return token
            if collision_type == "mask" and pygame.sprite.collide_mask(self.token, token):
                return token
        return tokens[0]

    def get_single_token_at_rect(self, rect: pygame.Rect) -> Optional["token_mod.Token"]:
        # Get first colliding token
        for token in self.board.tokens.sprites():
            if token.rect.colliderect(rect) and token != self.token:
                return token
        return None

    def get_tokens_at_rect(self, rect: pygame.Rect) -> list:
        """Returns all tokens that collide with a rectangle.

        Args:
            rect: A rectangle

        Returns all tokens in a rect
        """
        return [token for token in self.board.tokens if token.rect.colliderect(rect)]
