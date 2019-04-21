from miniworldmaker.tools import appearance
import pygame


class Background(appearance.Appearance):
    def __init__(self, board):
        super().__init__()
        self.parent = board
        self.register_action("grid", self.show_grid)
        self.register_action("scale_to_tile", self.scale_to_tile, begin = True)

    def next_sprite(self):
        super().next_sprite()
        self.parent.window.repaint_areas.append(self.image.get_rect())
        self.parent.window.window_surface.blit(self.image, (0, 0))

    @property
    def grid_overlay(self):
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


    def show_grid(self, image):
        i = 0
        while i <= self.parent.width:
            pygame.draw.rect(image, self.color, [i, 0, self.parent.tile_margin, self.parent.height])
            i += self.parent.tile_size + self.parent.tile_margin
        i = 0
        while i <= self.parent.height:
            pygame.draw.rect(image, self.color, [0, i, self.parent.width, self.parent.tile_margin])
            i += self.parent.tile_size + self.parent.tile_margin
        return image


    @property
    def is_scaled_to_tile(self):
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

    def scale_to_tile(self, image):
        image = pygame.transform.scale(image, (self.parent.tile_size, self.parent.tile_size))
        with_margin = pygame.Surface((self.parent.tile_size+self.parent.tile_margin, self.parent.tile_size+self.parent.tile_margin))
        with_margin.blit(image, (self.parent.tile_margin, self.parent.tile_margin))
        return with_margin
