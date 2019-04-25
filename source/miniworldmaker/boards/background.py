from miniworldmaker.tools import appearance
import pygame
from miniworldmaker.tools import image_renderers as ir


class Background(appearance.Appearance):
    def __init__(self, board):
        super().__init__()
        self.parent = board #: The parent of a Background is the associated board.
        self.register_action("grid", ir.ImageRenderer.show_grid)
        self.register_action("scale_to_tile", ir.ImageRenderer.scale_to_tile, begin = True)

    def next_sprite(self):
        super().next_sprite()
        self.parent.window.repaint_areas.append(self.image.get_rect())
        self.parent.window.window_surface.blit(self.image, (0, 0))

    @property
    def grid_overlay(self):
        """bool: Renders a grid overlay."""
        return self.enabled_image_actions["grid"]

    @grid_overlay.setter
    def grid_overlay(self, color=(255, 255, 255, 255)):
        if color is True:
            color = (200, 80, 60)
        if color is not False:
            self.color = color
            self.enabled_image_actions["grid"] = True
            self.call_action("grid")
            self.dirty = 1
        else:
            self.enabled_image_actions["grid"] = False
            self.call_action("grid")
            self.dirty = 1

    @property
    def is_scaled_to_tile(self):
        """bool: Scaled image to tile_size.

        Scales the image to Tile_size. This is needed if you want to texture the background on a Tiled_Board and want the texture to fill one tile at a time.
        """
        return self.enabled_image_actions["scale_to_tile"]

    @is_scaled_to_tile.setter
    def is_scaled_to_tile(self, value):
        if value is False:
            self.enabled_image_actions["scale_to_tile"] = False
        else:
            self.enabled_image_actions["scale_to_tile"] = True
            self.enabled_image_actions["scale"] = False
            self.enabled_image_actions["upscale"] = False
        self.call_image_actions["scale_to_tile"] = True
        self.dirty = 1
