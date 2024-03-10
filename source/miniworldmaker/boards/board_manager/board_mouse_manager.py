import pygame


class StageMouseManager:
    """ Handles collisions
    """

    def __init__(self, board):
        self.board = board
        self._mouse_position = None
        self._prev_mouse_position = None

    def update_positions(self):
        self._prev_mouse_position = self._mouse_position
        self._mouse_position = self.get_mouse_position()

    def get_mouse_position(self):
        pos = pygame.mouse.get_pos()
        clicked_container = self.board.app.container_manager.get_container_by_pixel(pos[0], pos[1])
        if clicked_container == self.board:
            return pos
        else:
            return None

    @property
    def mouse_position(self):
        return self.get_mouse_position()

    @property
    def prev_mouse_position(self):
        return self._prev_mouse_position

    def mouse_left_is_clicked(self):
        return pygame.mouse.get_pressed()[0]

    def mouse_right_is_clicked(self):
        return pygame.mouse.get_pressed()[0]
