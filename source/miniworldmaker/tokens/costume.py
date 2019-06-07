from miniworldmaker.tools import appearance
from miniworldmaker.tools import image_renderers as ir


class Costume(appearance.Appearance):

    def __init__(self, token):
        super().__init__()
        self.parent = token #: the parent of a costume is the associated token.
        self.is_upscaled = True
        self.is_rotatable = True
        self.register_action("info_overlay", ir.ImageRenderer.info_overlay)
        self.enable_action("orientation")

    def update(self):
        if self.parent.board:
            if self.parent.board.frame % self.animation_speed == 0:
                self.next_sprite()

    def set_costume(self, index):
        self._image_index = index

    @property
    def info_overlay(self):
        return self.enabled_image_actions["info_overlay"]

    @info_overlay.setter
    def info_overlay(self, value):
        """
        Shows info overlay (Rectangle around the token and Direction marker)
        Args:
            color: Color of info_overlay
        """
        if value is True:
            self.enable_action("info_overlay")
        else:
            self.disable_action("info_overlay")