import math
from typing import Union

import pygame
from miniworldmaker.board_positions import board_position
from miniworldmaker.board_positions import board_rect
from miniworldmaker.connectors import board_connector
from miniworldmaker.tokens import token


class PixelBoardConnector(board_connector.BoardConnector):
    """
    Connects pixelboard and pixeltokens
    """

    def __init__(self, token, board):
        super().__init__(token, board)
        self.token.size = (40, 40)

    def sensing_on_board(self, distance=0) -> bool:
        target_rect = self.get_destination_rect(distance)
        return target_rect.is_on_board()

    def sensing_borders(self, distance: int = 0 ) -> list:
        for i in range(distance + 1):
            target_rect = self.get_destination_rect(distance)
            borders = target_rect.borders()
        if borders:
            return borders
        else:
            return []

    def sensing_colors(self, colors: Union[tuple, list] = (), distance=0) -> list:
        if type(colors) == tuple:
            colors = [colors]
        line = self.get_line_in_direction(self.token.center, self.token.direction, distance)
        colorlist = self.board.get_colors_at_line(line)
        if not colors:
            return colorlist
        intersections = [value for value in colorlist if value in colors]
        return intersections

    def get_destination_rect(self, distance:int) -> board_rect.BoardRect:
        destination_rect = self.get_destination(self.token.position, self.token.direction, distance)
        destination_rect = board_position.BoardPosition(destination_rect[0], destination_rect[1])
        rect = destination_rect.to_rect(self.token.rect)
        rect.center= self.token.position
        return rect

    def get_token_rect(self) -> board_rect.BoardRect:
        if self.token.costume:
            _rect = self.token.image.get_rect()
            _rect.center = self.token.x, self.token.y
            return _rect
        else:
            return None

    def get_line_in_direction(self, start, direction, distance):
        return [self.get_destination(start, direction, i) for i in range(distance)]

    def get_line_to(self, start, target):
        sampling_rate = int(math.sqrt((target[0] - start[0]) ** 2 + target[1] - start[1] ** 2))
        x_spacing = (target[0] - start[0]) / (sampling_rate + 1)
        y_spacing = (target[1] - start[1]) / (sampling_rate + 1)
        return [board_position.BoardPosition(start[0] + i * x_spacing, start[1] + i * y_spacing) for i in
                range(1, sampling_rate + 1)]

    def get_destination(self, start, direction, distance) -> board_position.BoardPosition:
        exact_position_x = start.x + math.sin(math.radians(direction)) * distance
        exact_position_y = start.y - math.cos(math.radians(direction)) * distance
        return board_position.BoardPosition(exact_position_x, exact_position_y)

    @staticmethod
    def filter_actor_list(a_list, actor_type):
        return [actor for actor in a_list if type(Token) == actor_type]

    def sensing_tokens(self, token_type=None, distance: int = 1, collision_type="default") -> list:
            destination_rect = self.get_destination_rect(distance=distance)
            tokens = self.board.get_tokens_at_rect(destination_rect, singleitem=False, exclude=self.token,
                                                   token_type=token_type)
            if collision_type == "default":
                collision_type = "mask"
            if collision_type == "circle":
                tokenlist = [token for token in tokens if pygame.sprite.collide_circle(self.token, token)]
            elif collision_type == "rect" or collision_type == "static-rect":
                tokenlist = [token for token in tokens if pygame.sprite.collide_rect(self.token, token)]
            elif collision_type == "mask":
                tokenlist = [token for token in tokens if pygame.sprite.collide_mask(self.token, token)]
            return tokenlist

    def sensing_token(self, token_type=None, distance: int = 1) -> Union[token.Token, None]:
            destination_rect = self.get_destination_rect(distance)
            tokens = self.board.get_tokens_at_rect(destination_rect, singleitem=True, exclude=self.token,
                                                  token_type=token_type)
            if self.token.collision_type == "default":
                collision_type = "mask"
            if tokens:
                for token in tokens:
                    if collision_type == "circle":
                        if pygame.sprite.collide_circle(self.token, token):
                            return token
                    if collision_type == "rect" or collision_type == "static-rect":
                        if pygame.sprite.collide_rect(self.token, token):
                            return token
                    if collision_type == "mask":
                        if pygame.sprite.collide_mask(self.token, token):
                            return token
            return None

    def bounce_from_token(self, other):
        """experimental: Bounces actor from another token
        Args:
            token: the token

        Returns: the actor

        """
        angle = self.token.direction
        self.token.move(-self.token.speed)
        self.token.point_towards_token(other)
        incidence = self.token.direction - angle
        self.token.turn_left(180 - incidence)
        return self.token

    def set_size(self, value):
        if value!= self.token._size:
            self._old_size = self.token._size
            shift = (value[0] - self._old_size[0]) / 2,  (value[1] - self._old_size[1]) /2
            new_position = self.token._position[0] + shift[0], self.token._position[1] + shift[1]
            self.token.position = new_position
            self.token._size = value
            self.dirty = 1
            if hasattr(self, "costume"):
                self.costume.call_actions(["scale", "upscale"])
            if hasattr(self, "physics") and self.physics.started:
                self.physics.reload_physics()