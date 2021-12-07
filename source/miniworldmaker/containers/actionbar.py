import os
import pygame

from miniworldmaker.containers import container


class ActionBar(container.Container):
    """
    The actionbar is shown under the Board.

    It contains buttons to run, stop or run, reset or trigger a stepwise execution of program.

    The buttons are defined in Actionbar-Widgets

    """

    def __init__(self, board):
        super().__init__()
        self.widgets = []
        self.position = "right"
        self.board = board
        self._app = board.app
        self.listen_to_all_events = False
        self.add_widget(PlayButton(self.board))
        self.add_widget(RunButton(self.board))
        self.add_widget(ResetButton(self.board))
        self.add_widget(InfoButton(self.board))
        self.add_widget(SpeedDownButton(self.board))
        self.add_widget(SpeedLabel(self.board))
        self.add_widget(SpeedUpButton(self.board))
        self.board.is_running = False
        self.dirty = 1
        self.default_size = 80

    def add_widget(self, widget):
        """
        Adds a widget to the toolbar

        Args:
            widget: A toolbar widget

        Returns: the widget

        """
        widget.clear()
        widget.parent = self
        self.widgets.append(widget)
        self.dirty = 1
        widget.dirty = 1
        return widget

    def repaint(self):
        self.surface = pygame.Surface((self._container_width, self._container_height))
        if self.dirty:
            self.surface.fill((255, 255, 255))
            if self.widgets:
                actual_position = 5
                for widget in self.widgets:
                    widget.height = self._container_height - 10
                    widget.repaint()
                    self.surface.blit(widget.surface, (actual_position, 5))
                    actual_position += widget.width + 5  # 5 is padding between elements
                self.dirty = 0
                self.board._app.window.repaint_areas.append(self.rect)

    def _widgets_total_width(self):
        width = 0
        for widget in self.widgets:
            width += widget.width + 5
        return width - 5

    def get_event(self, event, data):
        if event == "mouse_left":
            actual_position = 5
            x, y = data[0], data[1]
            if self.is_in_container(x, y) and not x > self._widgets_total_width():
                for widget in self.widgets:
                    if actual_position + widget.width + 5 > x:
                        return widget.get_event(event, data)
                    else:
                        actual_position = actual_position + widget.width + 5
        elif event == "board_speed_changed":
            for widget in self.widgets:
                widget.get_event(event, data)
        else:
            return "no toolbar event"


class ActionBarWidget():
    """
    Base class of Actionbar-Widgets

    """

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
        self.package_directory = (os.path.join(
            os.path.dirname(os.path.abspath(__file__)), os.pardir))
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
        if event == "mouse_left":
            self.board.is_running = True
            self.board.stop(1)


class RunButton(ActionBarWidget):

    def __init__(self, board):
        super().__init__(board)
        self.set_text("Run")
        self.event = "button"
        if self.board.is_running:
            self.state = "running"
        else:
            self.state = "pause"

        self.set_image(self.path)
        self.data = self._text
        self.width = 80

    @property
    def path(self):
        if self.state == "pause":
            return os.path.join(self.package_directory, "resources", 'pause.png')
        else:
            return os.path.join(self.package_directory, "resources", 'run.png')

    def get_event(self, event, data):
        if event == "mouse_left":
            if not self.board.is_running:
                self.board.is_running = True
                self.state = "pause"
                self.set_image(self.path)
            else:
                self.board.is_running = False
                self.state = "running"
                self.set_image(self.path)
        self.parent.dirty = 1


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
        if event == "mouse_left":
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
        if event == "mouse_left":
            self.parent._app.event_manager.send_event_to_containers(self.event, self._text)
            for token in self.board.tokens:
                token.remove()
            self.board.reset()


class InfoButton(ActionBarWidget):

    def __init__(self, board):
        super().__init__(board)
        self.set_text("Info")
        self.event = "button"
        self.path = os.path.join(self.package_directory, "resources", 'question.png')
        self.set_image(self.path)
        self.data = self._text
        self.width = 80
        self.state = False

    def get_event(self, event, data):
        if event == "mouse_left":
            if self.state is False:
                for token in self.board.tokens:
                    token.costume.info_overlay = True
                    self.board.is_running = True
                    self.board.stop(1)
                    self.state = True

            else:
                for token in self.board.tokens:
                    token.costume.info_overlay = False
                    self.board.is_running = True
                    self.board.stop(1)
                    self.state = False


class SpeedLabel(ActionBarWidget):

    def __init__(self, board):
        super().__init__(board)
        self.set_text(str(board.fps))
        self.event = "button"
        self.data = self._text
        self.width = 30
        self.board = board

    def get_event(self, event, data):
        if event == "board_speed_changed":
            self._text = str(self.board.fps)
            self.dirty = 1


class SpeedDownButton(ActionBarWidget):

    def __init__(self, board, ):
        super().__init__(board)
        self.set_text("Speed down")
        self.event = "button"
        self.path = os.path.join(self.package_directory, "resources", 'left.png')
        self.set_image(self.path)
        self.data = self._text
        self.width = 30

    def get_event(self, event, data):
        if event == "mouse_left":
            self.board.fps -= 1
            self.parent._app.event_manager.send_event_to_containers(
                "board_speed_changed", self.board.fps)


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
        if event == "mouse_left":
            self.board.fps += 1
            self.parent._app.event_manager.send_event_to_containers(
                "board_speed_changed", self.board.fps)
