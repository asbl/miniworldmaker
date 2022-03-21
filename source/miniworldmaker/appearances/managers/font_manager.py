import pygame

from miniworldmaker.appearances import appearance


class FontManager:
    def __init__(self, appearance):
        self.font_size = 0  #: font_size if token-text != ""
        self.text_position = (0, 0)  #: Position of text relative to the top-left pixel of token
        self.font_path = None  #: Path to font-file
        self.font_style = "monospace"
        self.text = ""
        self.appearance = appearance

    def _get_font_object(self):
        font_size = 0
        font_size = self.font_size
        if self.font_path is None:
            font = pygame.font.SysFont(self.font_style, font_size)
        else:
            font = pygame.font.Font(self.font_path, font_size)
        return font

    def get_font_width(self):
        font = self._get_font_object()
        return font.size(self.text)[0]

    def transformation_write_text(self, image: pygame.Surface, parent, color) -> pygame.Surface:
        font = self._get_font_object()
        if self.appearance.parent.color == None:
            color = (255,255,255)
        else:
            color = self.appearance.parent.color
        label = font.render(self.text, 1, color)
        image.blit(label, self.text_position)
        return image
