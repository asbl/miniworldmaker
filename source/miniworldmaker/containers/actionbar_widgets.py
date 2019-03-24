import logging
import pygame
import os


class ActionBarWidget():
    log = logging.getLogger("toolbar")

    def __init__(self, board):
        self.myfont = pygame.font.SysFont("monospace", 15)
        self.background_color = (240, 240, 240)
        self.event = "no event"
        self.width = 0  # Set in Toolbar repaint
        self.height = 0  # Set in Toolbar repaint()
        self.parent = None
        self.board = board
        self.clear()

        self._text = ""
        self._image = None
        self._border = False
        self._text_padding = 5
        self._img_path = None
        self.surface = None
        self.package_directory = (os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
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
            image = pygame.transform.scale(image, (20, 20))
            self.surface.blit(image, (5, 5))
        if self._border:
            border_rect = pygame.Rect(0, 0, self.width, self.height - 2)
            pygame.draw.rect(self.surface, self.background_color, border_rect, self.width)
        self.dirty = 1

    def set_text(self, text):
        self._text = text
        self.dirty = 1

    def set_image(self, img_path):
        self._img_path = img_path
        self._text_padding = 30
        self.dirty = 1

    def set_border(self, color, width):
        self.border = True
        self.dirty = 1


class PlayButton(ActionBarWidget):

    def __init__(self, board):
        super().__init__(board)
        self.set_text("Act")
        self.event = "button"
        self.path = os.path.join(self.package_directory, "resources", 'play.png')
        self.set_image(self.path)
        self.data = self._text
        self.width = 70

    def get_event(self, event, data):
        self.board._act_all()


class RunButton(ActionBarWidget):

    def __init__(self, board):
        super().__init__(board)
        self.set_text("Run")
        self.event = "button"
        self.path = os.path.join(self.package_directory, "resources", 'run.png')
        self.set_image(self.path)
        self.data = self._text
        self.width = 80

    def get_event(self, event, data):
        if not self.board.is_running:
            self.board.is_running = True
            self.path = os.path.join(self.package_directory, "resources", 'pause.png')
            self.set_image(self.path)
        else:
            self.board.is_running = False
            self.path = os.path.join(self.package_directory, "resources", 'run.png')
            self.set_image(self.path)


class PauseButton(ActionBarWidget):

    def __init__(self, board):
        super().__init__(board)
        self.set_text("Pause")
        self.event = "button"
        self.path = os.path.join(self.package_directory, "resources", 'pause.png')
        self.set_image(self.path)
        self.data = self._text
        self.width = 90

    def get_event(self, event, data):
        self.parent.window.send_event_to_containers(self.event, self._text)


class ResetButton(ActionBarWidget):

    def __init__(self, board):
        super().__init__(board)
        self.set_text("Reset")
        self.event = "button"
        self.path = os.path.join(self.package_directory, "resources", 'reset.png')
        self.set_image(self.path)
        self.data = self._text
        self.width = 80

    def get_event(self, event, data):
        self.parent.window.send_event_to_containers(self.event, self._text)


class InfoButton(ActionBarWidget):

    def __init__(self, board):
        super().__init__(board)
        self.set_text("Info")
        self.event = "button"
        self.path = os.path.join(self.package_directory, "resources", 'question.png')
        self.set_image(self.path)
        self.data = self._text
        self.width = 80

    def get_event(self, event, data):
        self.parent.window.send_event_to_containers(self.event, self._text)


class SpeedLabel(ActionBarWidget):

    def __init__(self, board):
        super().__init__(board)
        self.set_text(str(board.speed))
        self.event = "button"
        self.data = self._text
        self.width = 30
        self.board = board

    def get_event(self, event, data):
        self.parent.window.send_event_to_containers(self.event, self._text)


class SpeedDownButton(ActionBarWidget):

    def __init__(self, board):
        super().__init__(board)
        self.set_text("Speed down")
        self.event = "button"
        self.path = os.path.join(self.package_directory, "resources", 'left.png')
        self.set_image(self.path)
        self.data = self._text
        self.width = 30

    def get_event(self, event, data):
        self.parent.window.send_event_to_containers(self.event, self._text)


class SpeedUpButton(ActionBarWidget):

    def __init__(self, board):
        super().__init__(board)
        self.set_text("Speed up")
        self.event = "button"
        self.path = os.path.join(self.package_directory, "resources", 'right.png')
        self.set_image(self.path)
        self.data = self._text
        self.width = 30

    def get_event(self, event, data):
        self.parent.window.send_event_to_containers(self.event, self._text)
