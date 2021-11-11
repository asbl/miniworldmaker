import miniworldmaker.tokens.positions.token_position_manager as token_positionmanager
import pygame


class TiledBoardPositionManager(token_positionmanager.TokenPositionManager):
    def __init__(self, token, position):
        super().__init__(token, position)
        
        
    def draw_position(self):
        return (self.token.x * self.token.board.tile_size, self.token.y * self.token.board.tile_size)

    @property
    def rect(self):
        return pygame.Rect(self.position[0] * self.size[0], self.position[1] * self.size[1], self.size[0], self.size[1])

    @property
    def size(self):
        return (self.token.board.tile_size,self.token.board.tile_size)

    @size.setter
    def size(self, value):
        raise Exception("You can't set size for tokens on a tiled board (size is always (1,1)")