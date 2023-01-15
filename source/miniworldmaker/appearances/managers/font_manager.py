import pygame


class FontManager:
    def __init__(self, appearance):
        self.font_size = 0  #: font_size if token-text != ""
        self.text_position = (0, 0)  #: Position of text relative to the top-left pixel of token
        self.font_path = None  #: Path to font-file
        self.font_style = "monospace"
        self.text = ""
        self.appearance = appearance

    def _get_font_object(self):
        font_size = self.font_size
        if self.font_path is None:
            font = pygame.font.SysFont(self.font_style, int(font_size))
        else:
            font = pygame.font.Font(self.font_path, font_size)
        return font

    def get_text_width(self):
        font = self._get_font_object()
        return font.size(self.text)[0]

    def get_text_height(self):
        font = self._get_font_object()
        return font.size(self.text)[1]

    def transformation_write_text(self, image: pygame.Surface, parent, color) -> pygame.Surface:
        # called from write_text in transformations_manager
        font = self._get_font_object()
        if not self.appearance.parent.color:
            color = (255, 255, 255)
        else:
            color = self.appearance.parent.color
        rendered_text = font.render(self.text, True, color)
        image.blit(rendered_text, self.text_position)
        return image

    def set_font_size(self, value, update=True):
        self.font_size = value
        if update:
            self.appearance.set_dirty("write_text", self.appearance.RELOAD_ACTUAL_IMAGE)
