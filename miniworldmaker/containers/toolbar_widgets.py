import pygame
import logging

class ToolbarWidget():

    log = logging.getLogger("toolbar")

    def __init__(self):
        self.myfont = pygame.font.SysFont("monospace", 15)
        self.background_color = (0,255,0)
        self.event = "no event"
        self.width = 0 # Set in Toolbar repaint
        self.height = 0 # Set in Toolbar repaint()
        self.parent = None
        self.clear()
        self.parent = None
        self._text = ""
        self._image = None
        self._border = False
        self._text_padding = 5
        self._img_path = None
        self.surface = None
        self._dirty = 1

    def get_event(self, event, data):
        self.parent.window.send_event_to_containers(self.event, 0)

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value
        if self.parent:
            self.parent.dirty = value

    def clear(self):
        self.surface = pygame.Surface((self.width, self.height))
        self.dirty = 1
        return self.surface

    def repaint(self):
        self.clear()
        self.draw_surface()

    def draw_surface(self):
        self.surface.fill(self.background_color)
        label = self.myfont.render(self._text, 1, (0, 0, 0))
        self.surface.blit(label, (self._text_padding, 5))
        if self._img_path is not None:
            image = pygame.image.load(self._img_path)
            image = pygame.transform.scale(image, (22, 22))
            self.surface.blit(image, (2, 0))
        if self._border:
            border_rect = pygame.Rect(0, 0, self.width, self.height - 2)
            pygame.draw.rect(self.surface, self.background_color, border_rect, self.width)
        self.dirty = 1

    def set_text(self, text):
        self._text = text
        self.dirty = 1

    def set_image(self, img_path):
        self._img_path = img_path
        self._text_padding = 25
        self.dirty = 1

    def set_border(self, color, width):
        self.border = True
        self.dirty = 1


class ToolbarButton(ToolbarWidget):

    log = logging.getLogger("toolbar-button")

    def __init__(self, text, img_path=None):
        super().__init__()
        self.set_text(text)
        self.event = "button"
        if img_path != None:
            self.set_image(img_path)
        self.data = text

    def get_event(self, event, data):

        self.parent.window.send_event_to_containers(self.event, self._text)


class ToolbarLabel(ToolbarWidget):

    def __init__(self,text, img_path = None):
        super().__init__()
        if img_path != None:
            self.set_image(img_path)
        self.set_text(text)
        self.event = "label"
        self.data = text