import miniworldmaker.tokens.costumes.token_costume_manager as token_costumemanager
import pygame


class TiledBoardCostumeManager(token_costumemanager.TokenCostumeManager):

    def set_size(self, value: tuple = (1, 1)):
        self.token._size = [self.token.board.tile_size, self.token.board.tile_size]