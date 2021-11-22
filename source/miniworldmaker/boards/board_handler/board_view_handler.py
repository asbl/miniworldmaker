import pygame
from miniworldmaker.appearances import appearances
from miniworldmaker.appearances import background


class BoardViewHandler:

    def __init__(self, board):
        self.board = board
        self.repaint_all: int = 1
        self.background = None
        self.surface: pygame.Surface = pygame.Surface((1, 1))
        self.has_background = False
        self.backgrounds: appearances.Backgrounds = appearances.Backgrounds(self.background)

    def init_background(self, background_image):
        if background_image is not None:
            self.add_background(background_image)
            self.has_background = True
        else:
            self.add_background(None)
            self.has_background = False

    def remove_background(self, background=None):
        if background != None:
            index = self.backgrounds.get_index(background)
            self.backgrounds.remove(index)
        else:
            self.backgrounds.remove(-1)

    def add_background(self, source):
        if not self.has_background and self.background != None:
            self.remove_background()
        if source is None:
            source = (255, 0, 255, 100)
        new_background = background.Background(self.board)
        if type(source) == str:
            new_background.add_image(source)
        elif type(source) == tuple:
            new_background.fill(source)
        if self.background is None or not self.has_background:
            self.background = new_background
            self.repaint_all = 1
            self.update_all_costumes()
            self.update_background()
        self.backgrounds.add(new_background)
        return new_background

    def switch_background(self, background):
        if type(background) == int:
            background = self.background.get_index(background)
        self.background = background
        self.repaint_all = 1
        [token.set_dirty() for token in self.tokens]
        return self.background

    def update_background(self):
        if self.background:
            self.background.update()

    def repaint(self):
        if self.background:
            if self.repaint_all:
                self.background.call_all_actions()
                self.surface = pygame.Surface(
                    (self.board.container_width, self.board.container_height))
                image = self.background.reload_image()
                self.surface.blit(image, self.surface.get_rect())
            self.board.tokens.clear(self.surface, self.image)
            repaint_rects = self.board.tokens.draw(self.surface)
            self.board.app.window.repaint_areas.extend(repaint_rects)
            if self.repaint_all:
                self.board.app.window.repaint_areas.append(self.board.rect)
                self.repaint_all = False

    def full_repaint(self):
        self.dirty = 1
        self.repaint_all = 1
        self.repaint()

    def find_colors(self, rect, color, threshold=(20, 20, 20, 20)):
        return self.background.count_pixels_by_color(rect, color, threshold)

    @property
    def image(self) -> pygame.Surface:
        if self.background:
            return self.background.image
        return pygame.Surface((1, 1))

    def update_all_costumes(self):
        [token.costume.update() for token in self.board.tokens]