import math
import pygame
from typing import Union


from miniworldmaker.board_positions import board_position, board_position_factory
from miniworldmaker.board_positions import board_rect_factory
from miniworldmaker.tokens.sensors import token_boardsensor as boardsensor
from miniworldmaker.tokens import token


class TokenPixelBoardSensor(boardsensor.TokenBoardSensor):
    """
    Connects pixelboard and pixeltokens
    """

    def __init__(self, token, board):
        super().__init__(token, board)

    def sensing_on_board(self, distance=0) -> bool:
        target_rect = self.get_destination_rect(distance)
        return self.board.position_handler.is_rect_completly_on_board(target_rect)

    def sensing_borders(self, distance: int = 0) -> list:
        """
        The function compares the rectangle (or alternatively the
        path that the rectangle of the object **distance** pixels travels)
        with the edges of the playing field.
        """
        borders = None
        for _ in range(distance + 1):
            target_rect = self.get_destination_rect(distance)
            borders = self.board.position_handler.get_borders_from_rect(target_rect)
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

    def get_destination_rect(self, distance: int) -> pygame.Rect:
        destination_pos = self.get_destination(self.token.position, self.token.direction, distance)
        destination_pos = board_position_factory.BoardPositionFactory(
            self.token.board).create(destination_pos)
        rect = board_rect_factory.BoardRectFactory(self.token.board).from_position(
            destination_pos, dimensions=self.token.size)
        rect.center = destination_pos
        return rect

    def get_line_in_direction(self, start, direction, distance):
        return [self.get_destination(start, direction, i) for i in range(distance)]

    def get_line_to(self, start, target):
        sampling_rate = int(math.sqrt((target[0] - start[0]) ** 2 + target[1] - start[1] ** 2))
        x_spacing = (target[0] - start[0]) / (sampling_rate + 1)
        y_spacing = (target[1] - start[1]) / (sampling_rate + 1)
        return [board_position_factory.BoardPositionFactory(self.token.board).create((start[0] + i * x_spacing, start[1] + i * y_spacing) for i in
                range(1, sampling_rate + 1))]

    def get_destination(self, start, direction, distance) -> board_position.BoardPosition:
        exact_position_x = start[0] + math.sin(math.radians(direction)) * distance
        exact_position_y = start[1] - math.cos(math.radians(direction)) * distance
        pos = board_position_factory.BoardPositionFactory(
            self.token.board).create((exact_position_x, exact_position_y))
        return pos

    @staticmethod
    def filter_actor_list(a_list, actor_type):
        return [actor for actor in a_list if type(token.Token) == actor_type]

    def sensing_tokens(self, token_filter=None, distance: int = 0, collision_type="default") -> list:
        # , singleitem: bool = False, exclude=None, token_type=None
        destination_rect = self.get_destination_rect(distance=distance)
        tokens = self.board.get_tokens_at_rect(destination_rect)
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

    def sensing_token(self, token_filter = None, distance: int = 0) -> Union["token.Token", None]:
        destination_rect = self.get_destination_rect(distance)
        tokens = self.board.get_single_token_at_rect(destination_rect)
        tokens = self.remove_self_from_token_list(tokens)
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
            if collision_type == "rect" or collision_type == "static-rect" and pygame.sprite.collide_rect(self.token, token):
                return token
            if collision_type == "mask" and pygame.sprite.collide_mask(self.token, token):
                return token
        return None
