import math
from typing import Union

import pygame
from boards import board_position
from boards import board_rect
from tokens import board_connector
from tokens import token


class PixelBoardConnector(board_connector.BoardConnector):
    """

    """

    def __init__(self, token, board):
        super().__init__(token, board)
        self.token.size = (40, 40)

    def sensing_on_board(self, distance=0) -> bool:
        target_rect = self.get_destination_rect(distance)
        return target_rect.is_on_board()

    def sensing_borders(self, distance: int = 0, ) -> list:
        for i in range(distance + 1):
            target_rect = self.get_destination_rect(distance)
            borders = target_rect.borders()
        else:
            return []

    def sensing_colors(self, distance=0, colors: Union[tuple, list] = ()) -> list:
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
        return rect

    def get_token_rect(self) -> board_rect.BoardRect:
        _rect = board_rect.BoardRect(0, 0, self.token.width, self.token.height)
        _rect.center = self.token.x + self.token.width / 2, self.token.y + self.token.height / 2
        return _rect

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
        return [actor for actor in a_list if type(actor) == actor_type]

    def sensing_tokens(self, distance: int = 1, token_type=None, exact=False) -> list:
        destination_rect = self.get_destination_rect(distance=distance)
        tokens = self.board.get_tokens_at_rect(destination_rect, singleitem=False, exclude=self, token_type=token_type)
        token_list = []
        for token in tokens:
            if exact and token:
                if pygame.sprite.collide_mask(self.token, token):
                    token_list.append(token)
            elif not exact and token:
                token_list.append(token)
        return token_list

    def sensing_token(self, distance: int = 1, token_type=None, exact=False) -> Union[token.Token, None]:
        destination_rect = self.get_destination_rect(distance)
        token = self.board.get_tokens_at_rect(destination_rect, singleitem=True, exclude=self, token_type=token_type)
        if exact and token:
            if pygame.sprite.collide_mask(self.token, token):
                return token
            else:
                return None
        return None

    def bounce_from_token(self, other):
        """experimental: Bounces actor from another token
        Args:
            token: the token

        Returns: the actor

        """
        angle = self.token.direction
        self.token.move(-self.token.fps)
        self.token.point_towards_token(other)
        incidence = self.token.direction - angle
        self.token.turn_left(180 - incidence)
        return self.token
