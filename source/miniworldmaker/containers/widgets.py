from tkinter import filedialog
from typing import Union
import tkinter as tk
import pygame
from miniworldmaker.tools import mwminspection


class Widget:
    """A Widget which can be placed in the Toolbar.

    A widget can have 'text' and an 'image'.
    """

    def __init__(self):
        self.myfont = pygame.font.SysFont("monospace", 15)
        self.event = "no event"
        self.parent = None
        self._text = ""
        self.speed = 1
        self._image = None

        self.surface = None
        self.timed = False
        self._dirty = 1
        # size and position
        self._width = 0  # Set in Toolbar repaint
        self._height = 30
        self._margin_bottom = 10
        self._margin_top = 0
        self._margin_left = 0
        self._margin_right = 0
        self.padding_left = 10
        self.padding_top = 5
        self.padding_bottom = 5
        self.padding_right = 0
        self.clear()
        # text
        self._text_padding_left = 5
        self._text_padding_top = 5
        self._text_align = "img"
        # background
        self._background_color = (200, 220, 220)
        # background-image
        self._img_width = 22
        self._img_source = None
        # border
        self._border = False
        self._border_width = 1
        self._border_color = (0, 0, 0, 255)
        self.on_setup()

    def on_setup(self):
        """Overwrite this method if you want to add custom setup-code"""
        pass

    def on_mouse_left(self, mouse_pos):
        pass

    @property
    def text_align(self) -> str:
        """text_align, 'img' or 'left'" """
        return self._text_align

    @text_align.setter
    def text_align(self, value: str):
        self._text_align = value
        self.dirty = 1

    @property
    def text_padding_left(self) -> int:
        """Left text_padding"""
        return self._text_padding_left

    @text_align.setter
    def text_padding_left(self, value: int):
        self._text_padding_left = value
        self.dirty = 1

    @property
    def text_padding_top(self) -> int:
        """Top text_padding"""
        return self._text_padding_top

    @text_padding_top.setter
    def text_padding_top(self, value: int):
        self._text_padding_top = value
        self.dirty = 1

    @property
    def text_padding_top_left(self) -> tuple:
        """Top-left text_padding"""
        return (self._text_padding_left, self.text_padding_top)

    @text_align.setter
    def text_padding_top_left(self, value: int):
        self._text_padding_top = value
        self._text_padding_left = value
        self.dirty = 1

    @property
    def img_width(self) -> float:
        """Width of image.
        (Height will be autoset by padding-left, padding-top and padding.right)
        """
        return self._img_width

    @img_width.setter
    def img_width(self, value: float):
        self._img_width = value
        self.dirty = 1

    @property
    def margin_bottom(self) -> int:
        """Margin below widget"""
        return self._margin_bottom

    @margin_bottom.setter
    def margin_bottom(self, value: int):
        self._margin_bottom = value
        self.dirty = 1

    @property
    def margin_top(self) -> int:
        """Margin above widget"""
        return self._margin_top

    @margin_top.setter
    def margin_top(self, value: int):
        self._margin_top = value
        self.dirty = 1

    @property
    def margin_left(self) -> int:
        """left margin"""
        return self._margin_left

    @margin_left.setter
    def margin_left(self, value: int):
        self._margin_left = value
        self.dirty = 1

    @property
    def margin_right(self) -> int:
        """right margin"""
        return self._margin_right

    @margin_right.setter
    def margin_right(self, value: int):
        self._margin_right = value
        self.dirty = 1

    @property
    def height(self) -> int:
        """Widget height"""
        return self._height

    @property
    def width(self) -> int:
        """Widget width (read only value)"""
        return self._width

    @height.setter
    def height(self, value: int):
        self._height = value

    @property
    def background_color(self) -> tuple:
        return self._background_color

    @background_color.setter
    def background_color(self, value: tuple):
        self.set_background_color(value)

    def set_background_color(self, value) -> "ToolbarWidget":
        self._background_color = value
        self.dirty = 1
        return self

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
        """Removes the widget from toolbar"""
        self.parent.widgets.remove(self)
        self.parent.dirty = 1

    def _repaint(self):
        """Repaints the widget."""
        if self.dirty == 1:
            self.clear()
            self.surface.fill(self.background_color)
            if self._img_source is not None:
                if type(self._img_source) == str:
                    image = pygame.image.load(self._img_source)
                if type(self._img_source) == tuple:
                    image = pygame.Surface((1, 1))
                    image.fill(self._img_source)
                image = pygame.transform.scale(
                    image, (self.img_width, self.height - self.padding_top - self.padding_bottom)
                )
                self.surface.blit(image, (self.padding_left, self.padding_top))
            if self._border:
                border_rect = pygame.Rect(0, 0, self.width, self.height)
                pygame.draw.rect(self.surface, self._border_color, border_rect, self._border_width)
            # Blit text to surface
            label = self.myfont.render(self._text, 1, (0, 0, 0))
            if self.text_align == "img":
                self.surface.blit(
                    label,
                    (
                        self.padding_left + self.img_width + self._text_padding_left,
                        self.padding_top + self._text_padding_top,
                    ),
                )
            if self.text_align == "left":
                self.surface.blit(
                    label, (self.padding_left + self._text_padding_left, self.padding_top + self.text_padding_top)
                )
        self.dirty = 0

    @property
    def text(self) -> str:
        """The text which is displayed on the widget."""
        return self._text

    @text.setter
    def text(self, value: str):
        self.set_text(value)

    def set_text(self, text: Union[str, int, float]):
        """Sets text of widget.

        int and float values are converted to string.
        """
        if type(text) == int or type(text) == float:
            text = str(text)
        self._text = text
        self.dirty = 1

    def set_image(self, _img_source: Union[str, tuple]):
        """sets image of widget

        Args:
            _img_source (str): path to image or tuple with color
        """
        self._img_source = _img_source
        self.dirty = 1

    def set_border(self, color: tuple = (0, 0, 0, 255), width: int = 1):
        """sets border of widget

        Args:
            color (_type_): _description_
            width (_type_): _description_
        """
        self._border = True
        self._border_color = color
        self._width = width
        self.dirty = 1

    def __str__(self):
        return "{0} : {1}".format(self.__class__.__name__, self._text)

    def register(self, method: callable) -> callable:
        """
        Used as decorator
        e.g.
        @register
        def method...
        """
        bound_method = mwminspection.MWMInspection(self).bind_method(method)
        return bound_method


class Button(Widget):
    """A Toolbar Button

    The Button can receive events.

    If the button is clicked

    Args:
        ToolbarWidget (_type_): _description_
    """

    def __init__(self, text, img_path=None):
        super().__init__()
        self.set_text(text)
        self.event = "button_pressed"
        if img_path != None:
            self.set_image(img_path)
        self.data = text

    def on_mouse_left(self, mouse_pos):
        """This event is called when the button is clicked -

        By default, a message with the button text is then sent to the board.

        Examples:

            Send a event on button-click:

            .. code-block:: python

                toolbar = Toolbar()
                button = ToolbarButton("Start Rocket")
                toolbar.add_widget(button)
                board.add_container(toolbar, "right")

                @board.register
                def on_message(self, message):
                    if message == "Start Rocket":
                        rocket.started = True
        """
        self.parent.send_message(self._text)


ToolbarButton = Button


class Label(Widget):
    def __init__(self, text, img_path=None):
        super().__init__()
        if img_path != None:
            self.set_image(img_path)
        self.set_text(text)
        self.event = "label"
        self.data = text
        self.background_color = (255, 255, 255, 0)


ToolbarLabel = Label


class SaveButton(Widget):
    def __init__(
        self,
        board,
        text,
        filename: str = None,
        img_path: str = None,
    ):
        super().__init__()
        if img_path != None:
            self.set_image(img_path)
        self.set_text(text)
        self.event = "label"
        self.data = text
        self.app = board.app
        self.file = filename
        self.tokens = None

    def on_mouse_left(self, event, data):
        if event == "mouse_left":
            if self.file is None:
                tk.Tk().withdraw()
                self.file = filedialog.asksaveasfilename(
                    initialdir="./", title="Select file", filetypes=(("db files", "*.db"), ("all files", "*.*"))
                )
                self.app.board.save_to_db(self.file)
                self.app.board.send_message("Saved new world", self.file)
            else:
                self.app.board.save_to_db(self.file)
                self.app.board.send_message("Saved new world", self.file)
                print("Board was saved to file:", self.file)


class LoadButton(Widget):
    def __init__(
        self,
        board,
        text,
        filename,
        img_path=None,
    ):
        super().__init__()
        if img_path != None:
            self.set_image(img_path)
        self.set_text(text)
        self.file = filename
        self.app = board.app

    def on_mouse_left(self, event, data):
        if event == "mouse_left":
            tk.Tk().withdraw()
            if self.file is None:
                self.file = filedialog.askopenfilename(
                    initialdir="./", title="Select file", filetypes=(("db files", "*.db"), ("all files", "*.*"))
                )
            new_board = self.app.board.load_board_from_db(self.file)


class ClearButton(Widget):
    def __init__(
        self,
        board,
        text,
        img_path=None,
    ):
        super().__init__()
        self.set_text(text)
        self.app = board.app

    def on_mouse_left(self, event, data):
        if event == "mouse_left":
            self.app.board.clear()


class CounterLabel(Widget):
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


class TimeLabel(Widget):
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


class FPSLabel(Widget):
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
