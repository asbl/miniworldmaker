import pygame
from miniworldmaker.windows import miniworldwindow as window


class BoardPosition:

    def __init__(self, pos):
        if type(pos) == int:
            raise TypeError("Board position requires a tuple: (x,y) as parameter, not an int value")
        self.x = pos[0]
        self.y = pos[1]
        self.board = window.MiniWorldWindow.board

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise TypeError("No Valid key for board position")

    def __eq__(self, other):
        """Overrides the default implementation"""
        return self.near(other, self.board.default_actor_speed-1)

    @classmethod
    def from_pixel(cls, position: tuple, board = None):
        if board == None:
            board = window.MiniWorldWindow.board
        column = (position[0] - board.tile_margin) // (board.tile_size + board.tile_margin)
        row = (position[1] - board.tile_margin) // (board.tile_size + board.tile_margin)
        return cls((column, row))

    def near(self, other, distance):
        if isinstance(other, tuple):
            other = BoardPosition(other)
        if isinstance(other, BoardPosition):
            if self.x <= other.x + distance \
                    and self.x >= other.x - distance \
                    and self.y <= other.y + distance \
                    and self.y >= other.y - distance:
                return True
        else:
            return False

    def to_tuple(self):
        return (self.x, self.y)

    def to_rect(self, rect: pygame.Rect = None) -> pygame.Rect:
        if rect is None:
            new_rect = pygame.Rect(0, 0, self.board.tile_size, self.board.tile_size)
        else:
            new_rect = pygame.Rect(0, 0, rect.width, rect.height)
        # board position to pixel
        pixel_x = self.x * self.board.tile_size + self.x * self.board.tile_margin + self.board.tile_margin
        pixel_y = self.y * self.board.tile_size + self.y * self.board.tile_margin + self.board.tile_margin
        new_rect.topleft = (pixel_x, pixel_y)
        return new_rect

    def to_surface(self, rect : pygame.Rect) -> pygame.Surface:
        if rect is None:
            new_surface = pygame.Surface(0, 0, self.board.tile_size, self.board.tile_size)
        else:
            new_surface = pygame.Rect(0, 0, rect.width, rect.height)
        # board position to pixel
        pixel_x = self.x * self.board.tile_size + self.x * self.board.tile_margin + self.board.tile_margin
        pixel_y = self.y * self.board.tile_size + self.y * self.board.tile_margin + self.board.tile_margin
        new_surface.topleft = (pixel_x, pixel_y)
        return new_surface

    def __str__(self):
        return str("Pos(" + str(self.x) + "," + str(self.y) + ")")

    def up(self, value : int):
        return BoardPosition((self.x, self.y-value))

    def down(self, value : int):
        return BoardPosition((self.x, self.y+value))

    def left(self, value : int):
        return BoardPosition((self.x-value, self.y))

    def right(self, value : int):
        return BoardPosition((self.x+value, self.y-value))

    def add(self, x, y):
        return BoardPosition((self.x+x, self.y+y))

    def to_pixel(self) -> tuple:
        rect = self.to_rect()
        return rect.topleft

    def is_on_board(self):
        if self.x > 0 and self.y > 0 and self.x < self.board.width and self.y < self.board.height:
            return True
        else:
            return False