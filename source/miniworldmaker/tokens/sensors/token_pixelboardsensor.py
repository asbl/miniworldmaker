import math
from typing import Union, Optional, List

import pygame

import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.board_positions.board_rect as board_rect
import miniworldmaker.boards.board as board_mod
import miniworldmaker.tokens.sensors.token_boardsensor as boardsensor
import miniworldmaker.tokens.token as token_mod
import miniworldmaker.tools.token_inspection as token_inspection

class TokenPixelBoardSensor(boardsensor.TokenBoardSensor):
    """Sensor for Tokens on PixelBoard.
    """

    def __init__(self, token: "token_mod.Token", board: "board_mod.Board"):
        super().__init__(token, board)

    def sensing_on_board(self, distance: int = 0) -> bool:
        return self.token.board.camera.is_token_in_viewport(self.token)

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

    def sense_color_at(self, direction: int = 0, distance: int = 1) -> list:
        if direction == 0:
            direction = self.token.direction
        destination = self.get_destination(self.token.center, direction, distance)
        return self.board.background.get_color(destination)

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
    def filter_actor_list(a_list, actor_type):
        return [actor for actor in a_list if type(token_mod.Token) == actor_type]

    def sensing_tokens(self, token_filter=None) -> list:
        tokens = pygame.sprite.spritecollide(self.token, self.token.board.camera.get_tokens_in_viewport(),  False, pygame.sprite.collide_rect)  
        tokens_list = self.remove_self_from_token_list(tokens)
        if tokens_list:
            tokens_list = self._detect_token(tokens_list, self.token.collision_type)
        if tokens_list:
            tokens_list = self.filter_token_list(tokens_list, token_filter)
        if tokens_list and len(tokens_list) >= 1:
            return tokens_list
        else: 
            return []

    def sensing_token(self, token_filter=None) -> Union["token_mod.Token", None]:
        token = pygame.sprite.spritecollideany(self.token, self.token.board.camera.get_tokens_in_viewport(), None)
        tokens_list = self.remove_self_from_token_list([token])
        if tokens_list:
            tokens_list = self._detect_token(tokens_list, self.token.collision_type)
        if tokens_list:
            tokens_list = self.filter_token_list(tokens_list, token_filter)
        if tokens_list and len(tokens_list) >= 1:
            return tokens_list[0]
        else: 
            return []
    
    def _detect_token(self, tokens, collision_type) -> List:
        tokens_list = []
        if collision_type == "circle":
            tokens_list = [
                token for token in tokens if pygame.sprite.collide_circle(self.token, token)]
        elif collision_type == "rect" or collision_type == "static-rect":
            tokens_list = [
                token for token in tokens if pygame.sprite.collide_rect(self.token, token)]
        elif collision_type == "mask":
            tokens_list = [
                token for token in tokens if pygame.sprite.collide_mask(self.token, token)]
        return tokens_list

    def sensing_tokens_at(self, direction: int = 0, distance: int = 1) -> list:
        if direction == 0:
            direction = self.token.direction
        destination = self.get_destination(self.token.center, direction, distance)
        return self.get_tokens_at_position(destination)

    def get_tokens_at_position(self, position):
        tokens = []
        for token in self.board.tokens:
            if token.get_global_rect().collidepoint(position[0], position[1]):
                tokens.append(token)
        if self.token in tokens:
            tokens.remove(self.token)
        return tokens
