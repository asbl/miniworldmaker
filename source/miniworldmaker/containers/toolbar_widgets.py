import logging
from tkinter import *
from tkinter import filedialog

import pygame


class ToolbarWidget():
    log = logging.getLogger("toolbar")

    def __init__(self):
        self.myfont = pygame.font.SysFont("monospace", 15)
        self.background_color = (200, 220, 220)
        self.event = "no event"
        self.width = 0  # Set in Toolbar repaint
        self.height = 0  # Set in Toolbar repaint()
        self.parent = None
        self.clear()
        self.parent = None
        self._text = ""
        self.speed = 1
        self._image = None
        self._border = False
        self._text_padding = 5
        self._img_path = None
        self.surface = None
        self.timed = False
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

    def remove(self):
        self.parent.widgets.remove(self)
        self.parent.dirty = 1

    def repaint(self):
        if self.dirty == 1:
            self.clear()
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
        self.dirty = 0

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

    def __str__(self):
        return "{0} : {1}".format(self.__class__.__name__, self._text)


class ToolbarButton(ToolbarWidget):
    log = logging.getLogger("toolbar-button")

    def __init__(self, text, img_path=None):
        super().__init__()
        self.set_text(text)
        self.event = "button_pressed"
        if img_path != None:
            self.set_image(img_path)
        self.data = text

    def get_event(self, event, data):
        print("send message", self.event, self._text)
        self.parent.window.send_event_to_containers(self.event, self._text)
        self.parent.window.send_event_to_containers("message", self._text)


class ToolbarLabel(ToolbarWidget):

    def __init__(self, text, img_path=None):
        super().__init__()
        if img_path != None:
            self.set_image(img_path)
        self.set_text(text)
        self.event = "label"
        self.data = text
        self.background_color = (255, 255, 255, 0)


class SaveButton(ToolbarWidget):

    def __init__(self, board, text, filename: str = None, img_path: str = None, ):
        super().__init__()
        if img_path != None:
            self.set_image(img_path)
        self.set_text(text)
        self.event = "label"
        self.data = text
        self.board = board
        self.file = filename

    def set_file(self):
        pass

    def get_event(self, event, data):
        if event == "mouse_left":
            if self.file is None:
                Tk().withdraw()
                try:
                    self.file = filedialog.asksaveasfilename(initialdir="./", title="Select file",
                                                             filetypes=(("db files", "*.db"), ("all files", "*.*")))
                    self.board.save_to_db(self.file)
                    self.board.window.send_event_to_containers("Saved new world", self.file)
                except:
                    print("Not saved!")
            else:
                self.board.save_to_db(self.file)
                self.board.window.send_event_to_containers("Saved new world", self.file)


class LoadButton(ToolbarWidget):

    def __init__(self, board, text, filename = None, img_path=None, ):
        super().__init__()
        if img_path != None:
            self.set_image(img_path)
        self.set_text(text)
        self.file = filename
        self.board = board

    def get_event(self, event, data):
        if event == "mouse_left":
            Tk().withdraw()
            if self.file is None:
                self.file = filedialog.askopenfilename(initialdir="./", title="Select file",
                                                       filetypes=(("db files", "*.db"), ("all files", "*.*")))
            self.board = self.board.__class__.from_db(self.file)
            self.board.window.send_event_to_containers("Loaded new world", self.file)
            self.board.show()


class CounterLabel(ToolbarWidget):

    def __init__(self, text, img_path=None):
        super().__init__()
        if img_path != None:
            self.set_image(img_path)
        self.value = 0
        self.text = text
        self.set_text("{0} : {1}".format(self.text, str(self.value)))
        self.data = str(0)

    def add(self, value):
        self.value += value
        self.set_text("{0} : {1}".format(self.text, str(self.value)))


class TimeLabel(ToolbarWidget):

    def __init__(self, board, text, img_path=None):
        super().__init__()
        if img_path != None:
            self.set_image(img_path)
        self.board = board
        self.value = self.board.frame
        self.text = text
        self.set_text("{0} : {1}".format(self.text, str(self.value)))
        self.data = str(0)
        self.timed = True

    def update(self):
        self.value = self.board.frame
        self.set_text("{0} : {1}".format(self.text, str(self.value)))


class FPSLabel(ToolbarWidget):

    def __init__(self, board, text, img_path=None):
        super().__init__()
        if img_path != None:
            self.set_image(img_path)
        self.board = board
        self.value = self.board.clock.get_fps()
        self.text = text
        self.set_text("{0} : {1}".format(self.text, str(self.value)))
        self.data = str(0)
        self.timed = True

    def update(self):
        self.value = self.board.clock.get_fps()
        self.set_text("{0} : {1}".format(self.text, str(self.value)))
