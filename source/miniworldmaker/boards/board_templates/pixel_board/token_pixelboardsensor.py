import math
from typing import Union, List

import miniworldmaker.boards.board_templates.pixel_board.board as board_mod
import miniworldmaker.positions.position as board_position
import miniworldmaker.positions.rect as board_rect
import miniworldmaker.positions.vector as board_vector
import miniworldmaker.tokens.managers.token_boardsensor as boardsensor
import pygame
from miniworldmaker.tokens import token as token_mod


class TokenPixelBoardSensor(boardsensor.TokenBoardSensor):
    """Sensor for Tokens on PixelBoard.
    """

    def __init__(self, token: "token_mod.Token", board: "board_mod.Board"):
        super().__init__(token, board)

    def is_token_on_the_board(self, distance: int = 0) -> bool:
        return self.token.board.camera.is_token_in_viewport(self.token)

    def detect_borders(self, distance: int = 0) -> list:
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

    def detect_color_at(self, direction: int = 0, distance: int = 1) -> list:
        if direction == None:
            direction = self.token.direction
        destination = self.get_destination(self.token.center, direction, distance)
        return self.board.background.get_color(destination)

    def get_destination_rect(self, distance: int) -> "board_rect.Rect":
        destination_pos = self.get_destination(self.token.position, self.token.direction, distance)
        destination_pos = board_position.Position.create(destination_pos)
        rect = board_rect.Rect.from_position(destination_pos, dimensions=self.token.size, board=self.board)
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

    def detect_tokens(self, token_filter) -> list:
        self.token.board.init_display()
        group = pygame.sprite.Group(self.token.board.camera.get_tokens_in_viewport())
        tokens = pygame.sprite.spritecollide(self.token, group, False,
                                             pygame.sprite.collide_rect)
        group.empty()
        detected_tokens = self._remove_self_from_token_list(tokens)
        if detected_tokens:
            detected_tokens = self._detect_token_by_collision_type(detected_tokens, self.token.collision_type)
        return self.filter_tokens(detected_tokens, token_filter)

    def detect_token(self, token_filter) -> Union["token_mod.Token", None]:
        self.token.board.init_display()
        group = pygame.sprite.Group(self.token.board.camera.get_tokens_in_viewport())
        tokens = pygame.sprite.spritecollide(self.token, group, False,
                                             pygame.sprite.collide_rect)
        group.empty()
        detected_tokens = self._remove_self_from_token_list(tokens)
        if detected_tokens:
            detected_tokens = self._detect_token_by_collision_type(detected_tokens, self.token.collision_type)
        del tokens
        return self.filter_first_token(detected_tokens, token_filter)

    def _detect_token_by_collision_type(self, tokens, collision_type) -> List:
        if collision_type == "circle":
            return [
                token for token in tokens if pygame.sprite.collide_circle(self.token, token)]
        elif collision_type == "rect" or collision_type == "static-rect":
            return [
                token for token in tokens if pygame.sprite.collide_rect(self.token, token)]
        elif collision_type == "mask":
            return [
                token for token in tokens if pygame.sprite.collide_mask(self.token, token)]

    def get_tokens_at_position(self, position):
        tokens = []
        for token in self.board.tokens:
            if token.get_global_rect().collidepoint(position[0], position[1]):
                tokens.append(token)
        if self.token in tokens:
            tokens.remove(self.token)
        return tokens

    def get_distance_to(self, obj: Union["token_mod.Token", "board_position.Position", tuple]) -> float:
        if isinstance(obj, token_mod.Token):
            vec = board_vector.Vector.from_tokens(self.token, obj)
        else:
            vec = board_vector.Vector.from_token_and_position(self.token, obj)
        return vec.length()
