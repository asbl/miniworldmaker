import pygame


class Appearance:

    def __init__(self):
        self.dirty = 0
        self.parent = None
        self.images_list = []  # Original images
        self._image_index = 0  # current_image index (for animations)
        self._images_dict = {}  # dict with key: image_path, value: loaded image
        self._image_paths = []  # list with all images
        # properties
        self.size = (5, 5)
        self.direction = 0
        self.cell_width = 0
        self.cell_height = 0
        self.cell_margin = 0
        self._image = pygame.Surface(self.size)
        self._image.fill((255, 0, 0, 255))
        self.image_actions = ["orientation", "scale", "upscale", "flip", "rotate", "colorize", "grid", "info_overlay"]
        self.enabled_image_actions = {"orientation": False,
                                      "scale": False,
                                      "upscale": False,
                                      "flip": False,
                                      "rotate": False,
                                      "colorize": False,
                                      "grid": False,
                                      "info_overlay": False}
        self.call_image_actions = {key: False for key in self.image_actions}
        self.image_handlers = {"orientation": self.correct_orientation,
                               "scale": self.scale,
                               "upscale": self.upscale,
                               "flip": self.flip,
                               "rotate": self.rotate,
                               "colorize": self.colorize,
                               "grid": self.grid_overlay,
                               "info_overlay": self.info_overlay}
        self.animation_speed = 60
        self._is_scaled = False
        self._is_upscaled = False
        self._is_animated = False
        self._is_flipped = False
        self._is_rotatable = False
        self._orientation = False
        self.is_scaled = True
        self.color = (255, 255, 255, 255)

    @property
    def is_upscaled(self):
        return self._is_upscaled

    @is_upscaled.setter
    def is_upscaled(self, value):
        self._is_upscaled = value
        if value is True:
            self.enabled_image_actions["scale"] = False
            self.enabled_image_actions["upscale"] = True
        else:
            self.enabled_image_actions["upscale"] = False
        self.dirty = 1

    @property
    def is_rotatable(self):
        return self._is_rotatable

    @is_rotatable.setter
    def is_rotatable(self, value):
        self._is_rotatable = value
        if value is True:
            self.enabled_image_actions["rotate"] = True
        else:
            self.enabled_image_actions["rotate"] = False
        self.dirty = 1

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value
        if value != 0:
            self.enabled_image_actions["orientation"] = True
        else:
            self.enabled_image_actions["orientation"] = False
        self.dirty = 1

    @property
    def is_flipped(self):
        return self._is_flipped

    @is_flipped.setter
    def is_flipped(self, value):
        self._is_flipped = value
        if value is True:
            self.enabled_image_actions["flip"] = True
        else:
            self.enabled_image_actions["flip"] = False
        self.dirty = 1

    @property
    def is_scaled(self):
        return self._is_scaled

    @is_scaled.setter
    def is_scaled(self, value):
        if value == True:
            self.enabled_image_actions["upscale"] = False
            self.enabled_image_actions["scale"] = True
        else:
            self.enabled_image_actions["scale"] = True
        self.call_image_actions["scale"] = True
        self.dirty = 1

    def add_image(self, img_path: str) -> int:
        if img_path in self._images_dict.keys():
            # load image from img_dict
            _image = self._images_dict[img_path]
        else:
            # create new image and add to img_dict
            if self.__class__.__name__ == "Background":
                _image = pygame.image.load(img_path).convert()
            else:
                _image = pygame.image.load(img_path).convert_alpha()
            self._images_dict[img_path] = _image
        self.images_list.append(_image)
        self._image_paths.append(img_path)
        self.dirty = 1
        return len(self.images_list) - 1

    @property
    def image(self) -> pygame.Surface:
        if self.dirty == 1:
            if self.images_list and self.images_list[self._image_index]:
                image = self.images_list[self._image_index]
            else:
                image = pygame.Surface(self.size)
                image.fill((0, 0, 255, 255))
            for action in self.image_actions:
                if self.dirty == 1:
                    if self.enabled_image_actions[action]:
                        if action in self.image_handlers.keys():
                            image = self.image_handlers[action](image)
            self._image = image
            self.call_image_actions = {key: False for key in self.call_image_actions}
            self.dirty = 0
        return self._image

    def next_sprite(self):
        if self._image_index < len(self.images_list) - 1:
            self._image_index = self._image_index + 1
        else:
            self._image_index = 0
        self.dirty = 1



    @property
    def is_animated(self):
        return self._is_animated

    @is_animated.setter
    def is_animated(self, value):
        self._is_animated = value

    def color_at_rect(self, rect, color, threshold=(0, 0, 0, 0)):
        cropped = pygame.Surface((rect.width, rect.height))
        cropped.blit(self._image, (0, 0), rect)
        return pygame.transform.threshold(dest_surf=None,
                                          set_behavior=0,
                                          surf=cropped,
                                          search_color=color,
                                          threshold=threshold)

    def color_at(self, position):
        position, self.size, self._image.get_at(position)
        return self._image.get_at(position)

    def upscale(self, image):
        size = self.size
        if size != 0:
            scale_factor_x = size[0] / image.get_width()
            scale_factor_y = size[1] / image.get_height()
            max_scale = max(scale_factor_x, scale_factor_y)
            scale_factor = min(scale_factor_x, scale_factor_y)
            new_width = int(image.get_width() * scale_factor)
            new_height = int(image.get_height() * scale_factor)
            image = pygame.transform.scale(image, (new_width, new_height))
        return image

    def scale(self, image):
        image = pygame.transform.scale(image, self.size)
        return image

    def rotate(self, image):
        return pygame.transform.rotate(image, self.direction)

    def correct_orientation(self, image):
        return pygame.transform.rotate(image, self.orientation)

    def changed_all(self):
        self.call_image_actions = {key: True for key in self.call_image_actions}
        self.dirty = 1

    def call_action(self, action):
        self.call_image_actions[action] = True
        self.dirty = 1

    def flip(self, image) -> pygame.Surface:
        return pygame.transform.flip(image, False, self._is_flipped)

    def colorize(self, image):
        """
        Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
        original).
        :param image: Surface to create a colorized copy of
        :param newColor: RGB color to use (original alpha values are preserved)
        :return: New colorized Surface instance
        """
        image = image.copy()
        # zero out RGB values
        image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        # add in new RGB values
        image.fill(self.color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
        return image

    def grid_overlay(self, image):
        i = 0
        print("grid", self.parent, self.__class__.__name__)
        width, height, tile_size, tile_margin, grid_color = self.parent.width, self.parent.height, self.parent.tile_size, self.parent.tile_margin, self.color
        print(width, height)
        while i <= width:
            pygame.draw.rect(image, grid_color, [i, 0, tile_margin, height])
            i += tile_size + tile_margin
        i = 0
        while i <= height:
            pygame.draw.rect(image, grid_color, [0, i, width, tile_margin])
            i += tile_size + tile_margin
        return image

    def info_overlay(self, image):
        pygame.draw.rect(image, self.color,
                         (0, 0, image.get_rect().width, image.get_rect().height), 10)
        # draw direction marker on image
        rect = image.get_rect()
        center = rect.center
        x = rect.right
        y = rect.centery
        pygame.draw.line(image, self.color, (center[0], center[1]), (x, y))
        return image

    def crop_image(self, image):
        cropped_surface = pygame.Surface(self.parent.size)
        cropped_surface.fill((255, 255, 255))
        cropped_surface.blit(image, (0, 0), (0, 0, self.parent.size[0], self.parent.size[1]))
        return cropped_surface

    def set_text(self, image, text):
        my_font = pygame.font.SysFont("monospace", self.parent.size)
        label = my_font.render(text, 1, (0, 0, 0))
        image.blit(label, (0, 0))
        return image
