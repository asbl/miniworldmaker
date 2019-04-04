from tools import image_renderer
import pygame


class Appearance:

    def __init__(self):
        self.dirty = 0
        self.changed = dict()
        self._renderer = image_renderer.ImageRenderer()
        self.images_list = []  # Original images
        self._image_index = 0  # current_image index (for animations)
        self._images_dict = {}  # dict with key: image_path, value: loaded image
        self._image_paths = []  # list with all images
        # properties
        self.size = (5, 5)
        self._image = pygame.Surface(self.size)
        self._image.fill((255, 0, 0, 255))
        self.image_actions = ["scale", "upscale"]
        self.changed = {"scale": False, "upscale": False}
        self.image_handlers = {"scale": self.scale, "upscale": self.upscale}
        self.animation_speed = 60
        self._is_scaled = False
        self._is_upscaled = False
        self._is_animated = False
        self.is_scaled = True

    @property
    def is_upscaled(self):
        return self._is_upscaled

    @is_upscaled.setter
    def is_upscaled(self, value):
        self._is_upscaled = value
        if value is True:
            if "scale" in self.image_actions:
                self.image_actions.remove('scale')
            if "upscale" not in self.image_actions:
                self.image_actions.append("upscale")
        self.dirty = 1

    @property
    def is_scaled(self):
        return self._is_scaled

    @is_scaled.setter
    def is_scaled(self, value):
        if value == True:
            if "upscale" in self.image_actions:
                self.image_actions.remove("upscale")
            if "scale" not in self.image_actions:
                self.image_actions.append("scale")
        self.changed["scale"] = True
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
                if self.__class__.__name__ == "Costume":
                    print("il", self.images_list)
                    print("ii", self._image_index)
                image = self.images_list[self._image_index]
            else:
                image = pygame.Surface(self.size)
                image.fill((0, 0, 255, 255))
            if self.__class__.__name__ == "Costume":
                print(self.changed)
            for action in self.changed:
                if self.changed[action] is True and action in self.image_actions:
                    if action in self.image_handlers.keys():
                        image = self.image_handlers[action](image)
            self._image = image
            self.changed = {key: False for key in self.changed}
            self.dirty = 0
            if self.__class__.__name__ == "Costume":
                print("is", self._image)
        if self.__class__.__name__ == "Costume":
            print("ind", self._image)
        return self._image


    def next_sprite(self):
        self._renderer.next_sprite()

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

    def changed_all(self):
        self.changed = {key: True for key in self.changed}
        self.dirty = 1
