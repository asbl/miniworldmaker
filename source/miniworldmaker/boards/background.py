from miniworldmaker.tools import appearance
import pygame

class Background(appearance.Appearance):
    def __init__(self, board):
        super().__init__()
        self.parent = board
        self.register_action("grid", self.grid_overlay)
        self.register_action("texture", self.texture, begin = True)
        self._is_textured = False

    def next_sprite(self):
        super().next_sprite()
        self.parent.window.repaint_areas.append(self.image.get_rect())
        self.parent.window.window_surface.blit(self.image, (0, 0))

    def show_grid(self, color=(255, 255, 255, 255)):
        self.dirty = 1
        self.color = color
        self.enabled_image_actions["grid"] = True
        self.call_action("grid")

    def texture(self, image):
        background = pygame.Surface(self.parent.size)
        background.fill((255, 255, 255))
        image = pygame.transform.scale(image, (self.parent.tile_size, self.parent.tile_size))
        for i in range(self.parent.width):
            for j in range(self.parent.height):
                width = i * self.parent.tile_size +i * self.parent.tile_margin
                height = j * self.parent.tile_size +j * self.parent.tile_margin
                background.blit(image, (width, height))
        self._image = background
        return background


    def grid_overlay(self, image):
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
    def is_textured(self):
        return self._is_textured

    @is_textured.setter
    def is_textured(self, value):
        self._is_textured = True
        if value is True:
            self.enabled_image_actions["upscale"] = False
            self.enabled_image_actions["scale"] = False
            self.enabled_image_actions["texture"] = True
        self.call_image_actions["texture"] = True
        self.dirty = 1