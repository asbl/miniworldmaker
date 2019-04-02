import pygame
from miniworldmaker.boards.board import Board
from miniworldmaker.tokens.token import Token


class PixelBoard(Board):

    def __init__(self, columns=40, rows=40):
        super().__init__(columns=columns, rows=rows)
        self._collision_partners_dict = dict()
        self._collision_partners = dict
        self._last_collisions = set()
        self.steps = 3

    def add_collision_partner(self, partner1, partner2):
        self._collision_partners_dict[partner1.token_id].add(partner2)
        self._collision_partners_dict[partner2.token_id].add(partner1)

    def add_to_board(self, token: Token, position) -> Token:
        """
        Overwrites add_actor in gamegrid
        :param token: The actor to be added
        :param position: The position where the actor should be placed in the grid
        :return: The reference to the Actor object
        """
        super().add_to_board(token, position)
        if token.size == (0, 0):
            token.size = (30, 30)
        self._collision_partners_dict[token.token_id] = pygame.sprite.Group()
        return token

    def remove_from_board(self, token: Token):
        token_id = token.token_id
        del self._collision_partners_dict[token_id]
        super().remove_from_board(token)

    def _call_collision_events(self):
        new_col_pairs = []
        for partner1 in self.tokens:
            if partner1.token_id in self._collision_partners_dict:
                collisions = pygame.sprite.spritecollide(partner1,
                                                         self._collision_partners_dict[partner1.token_id], False)
                for partner2 in collisions:
                    if (partner1, partner2) not in self._last_collisions:
                        partner1.get_event("collision", partner2)
                    new_col_pairs.append((partner1, partner2))
                if collisions:
                    pass
                for pair in new_col_pairs:
                    self.window.send_event_to_containers("collision", pair)

        self._last_collisions = set(new_col_pairs)

    def test_collision(self, actor1, actor2) -> bool:
        if actor1 is not actor2:
            if actor1.rect.colliderect(actor2.rect):
                return True
            else:
                return False

    def borders(self, rect):
        borders = []
        if rect.topleft[0] <= 0:
            borders.append("left")
        if rect.topleft[1] + rect.height >= self.height:
            borders.append("bottom")
        if rect.topleft[0] + rect.width >= self.width:
            borders.append("right")
        if rect.topleft[1] <= 0:
            borders.append("top")
        return borders

    def get_touching_borders(self, rect) -> list:
        borders = []
        if rect.topleft[0] <= 0:
            borders.append("left")
        if rect.topleft[1] + rect.height >= self.height:
            borders.append("bottom")
        if rect.topleft[0] + rect.width >= self.width:
            borders.append("right")
        if rect.topleft[1] <= 0:
            borders.append("top")
        return borders
