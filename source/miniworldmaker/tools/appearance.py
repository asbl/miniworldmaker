import pygame
from miniworldmaker.tools import image_renderers
from tools import image_renderers as ir


class Appearance:

    _images_dict = {}  # dict with key: image_path, value: loaded image

    def __init__(self):
        self.dirty = 0
        self.parent = None
        self.images_list = []  # Original images
        self._image_index = 0  # current_image index (for animations)
        self.image_paths = []  # list with all images
        # properties
        self._image = pygame.Surface((5,5))
        self.call_image_actions = {}
        self.image_actions = []
        self.enabled_image_actions = {}
        self.image_handlers = {}
        self.register_action("texture", ir.ImageRenderer.texture, begin=True)
        self.register_action("orientation", ir.ImageRenderer.correct_orientation)
        self.register_action("write_text", ir.ImageRenderer.write_text)
        self.register_action("scale", ir.ImageRenderer.scale)
        self.register_action("upscale", ir.ImageRenderer.upscale)
        self.register_action("flip", ir.ImageRenderer.flip)
        self.register_action("rotate", ir.ImageRenderer.rotate)
        self.register_action("colorize", ir.ImageRenderer.colorize)
        self.animation_speed = 60
        self._is_scaled = False
        self._is_upscaled = False
        self._is_animated = False
        self._is_flipped = False
        self._is_rotatable = False
        self._orientation = False
        self._is_textured = False
        self._is_scaled = True
        self._text = ""
        self.fill_color = (0,0,255,255)
        self.font_size = 0
        self.text_position = (0,0)
        self.font_path = None
        self.color = (255, 255, 255, 255)

    def register_action(self, action : str, handler, begin = False):
        if not begin:
            self.image_actions.append(action)
        else:
            self.image_actions.insert(0, action)
        self.image_handlers[action] = handler
        self.enabled_image_actions[action] = False

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
        """
        If is_rotatable is True, the image is rotated with actor direction.
        """
        return self._is_rotatable

    @is_rotatable.setter
    def is_rotatable(self, value):
        self._is_rotatable = value
        if value is True:
            self.enable_action("rotate")
        else:
            self.disable_action("rotate")

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value
        if value != 0:
            self.enable_action("orientation")
        else:
            self.disable_action("orientation")

    @property
    def is_flipped(self):
        return self._is_flipped

    @is_flipped.setter
    def is_flipped(self, value):
        self._is_flipped = value
        if value is True:
            self.enable_action("flip")
        else:
            self.disable_action("flip")

    @property
    def is_scaled(self):
        return self._is_scaled

    @is_scaled.setter
    def is_scaled(self, value):
        if value == True:
            self.disable_action("upscale")
            self.enable_action("scale")
        else:
            self.disable_action("scale")


    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        """
        Shows info overlay (Rectangle around the token and Direction marker)
        Args:
            color: Color of info_overlay
        """
        if value == "" or value is None:
            self.text = ""
            self.disable_action("write_text")
        else:
            self._text = value
            self.enable_action("write_text")

    def add_image(self, img_path: str) -> int:
        if img_path in Appearance._images_dict.keys():
            # load image from img_dict
            _image = Appearance._images_dict[img_path]
        else:
            # create new image and add to img_dict
            if self.__class__.__name__ == "Background":
                _image = pygame.image.load(img_path).convert()
            else:
                _image = pygame.image.load(img_path).convert_alpha()
                Appearance._images_dict[img_path] = _image
        self.images_list.append(_image)
        self.image_paths.append(img_path)
        self.dirty = 1
        return len(self.images_list) - 1

    @property
    def image(self) -> pygame.Surface:
        if self.dirty == 1:
            if self.images_list and self.images_list[self._image_index]:
                image = self.images_list[self._image_index]
            else:
                image = pygame.Surface(self.parent.size, pygame.SRCALPHA)
                image.fill(self.fill_color)
                image.set_alpha(255)
            for action in self.image_actions:
                if self.dirty == 1:
                    if self.enabled_image_actions[action]:
                        if action in self.image_handlers.keys():
                            image = self.image_handlers[action](image, parent = self.parent, appearance = self)
                    self.parent.dirty = 1
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
        self.parent.dirty = 1

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
        position, self.parent.size, self._image.get_at(position)
        return self._image.get_at(position)

    def changed_all(self):
        self.call_image_actions = {key: True for key in self.call_image_actions}
        self.dirty = 1

    def call_action(self, action):
        self.call_image_actions[action] = True
        self.dirty = 1
        self.parent.dirty = 1

    def enable_action(self, action):
        self.enabled_image_actions[action] = True
        self.call_action(action)
        self.parent.dirty = 1
        self.dirty = 1

    def disable_action(self, action):
        self.enabled_image_actions[action] = False
        self.call_action(action)
        self.parent.dirty = 1
        self.dirty = 1
