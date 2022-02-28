import pygame


class FontManager:
    def __init__(self):
        self.font_size = 0  #: font_size if token-text != ""
        self.text_position = (0, 0)  #: Position of text relative to the top-left pixel of token
        self.font_path = None  #: Path to font-file
        self.font_style = "monospace"
        self.text = ""

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
        label = font.render(self.text, 1, color)
        image.blit(label, self.text_position)
        return image
