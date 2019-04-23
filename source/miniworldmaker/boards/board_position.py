from miniworldmaker.windows import miniworldwindow as window
import pygame


class BoardPosition:

    def __init__(self, x, y):
        self.x = x
        self.y = y
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
    def from_pixel(cls, board, position: tuple):
        column = (position[0] - board.tile_margin) // (board.tile_size + board.tile_margin)
        row = (position[1] - board.tile_margin) // (board.tile_size + board.tile_margin)
        return cls(column, row)


    def near(self, other, distance):
        if isinstance(other, tuple):
            other = BoardPosition(other[0], other[1])
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

    def __str__(self):
        return str("Pos(" + str(self.x) + "," + str(self.y) + ")")

    def up(self, value : int):
        return BoardPosition(self.x, self.y-value)

    def down(self, value : int):
        return BoardPosition(self.x, self.y+value)

    def left(self, value : int):
        return BoardPosition(self.x-value, self.y)

    def right(self, value : int):
        return BoardPosition(self.x+value, self.y-value)

    def add(self, x, y):
        return BoardPosition(self.x+x, self.y+y)

