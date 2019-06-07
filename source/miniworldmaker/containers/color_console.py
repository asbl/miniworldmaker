import os
import pygame
from miniworldmaker.containers import container


class ColorConsole(container.Container):
    event_id = 0

    def __init__(self, board):
        super().__init__()
        self._lines = 0
        self._height = self._lines * 20
        self._text_queue = []
        self.listen_to_all_events = True
        self.margin_first = 10
        self.margin_last = 5
        self.row_height = 25
        self.row_margin = 10
        self.margin_left = 10
        self.margin_right = 10
        self._dirty = 1
        self.board = board

    def repaint(self):
        if self.dirty:
            self.surface.fill((255, 255, 255))
            package_directory = os.path.dirname(os.path.abspath(__file__))
            myfont = pygame.font.SysFont("monospace", 15)
            for i, text in enumerate(self._text_queue):
                row = pygame.Surface((self.width - (self.margin_left + self.margin_right), self.row_height))
                row.fill((200, 200, 200))
                label = myfont.render(text, 1, (0, 0, 0))
                row.blit(label, (10, 5))
                self.surface.blit(row, (self.margin_left, self.margin_first + i * 20 + i * self.row_margin))

    @property
    def lines(self):
        _lines = int(self.height - self.margin_first - self.margin_last) / (self.row_height)
        return _lines

    def get_event(self, event, data):
        if event == "mouse_left":
            self.event_id += 1
            text = self.board.get_color_at_board_position(self.board.get_board_position_from_pixel(data))
            self._text_queue.append(str(text))
            if len(self._text_queue) > self.lines:
                self._text_queue.pop(0)
            self.dirty = 1
