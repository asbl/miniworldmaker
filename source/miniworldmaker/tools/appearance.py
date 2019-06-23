import pygame
from miniworldmaker.boards import board_position
from miniworldmaker.tools import image_renderers as ir


class Appearance:
    """ Base class of token costumes and board backgrounds

    Die Klasse enthält alle Methoden und Attribute um Bilder der Objekte anzuzeigen, zu animieren, Text auf den Bildern zu rendern  oder Overlays anzuzeigen.

    """

    def __init__(self):
        self.dirty = 0
        self.blit_images = [] # Images which are blitted on the background
        self.parent = None
        self.images_list = []  # Original images
        self._image_index = 0  # current_image index (for animations)
        self.image_paths = []  # list with all images
        # properties
        self.raw_surface = pygame.Surface((1, 1)) # size set in image()-method
        self._image = pygame.Surface((1,1)) # size set in image()-method
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
        self.animation_speed = 60 #: The animation speed for animations
        self._is_animated = False
        self._is_flipped = False
        self._orientation = 90
        self._text = ""
        self.fill_color = (0, 0, 255, 255) #: background_color if actor has no background image
        self.font_size = 0 #: font_size if token-text != ""
        self.text_position = (0, 0) #: Position of text relative to the top-left pixel of token
        self.font_path = None #: Path to font-file
        self.color = (255, 255, 255, 255) #: color for overlays
        self.dirty = 1
        self.surface_loaded = False
        self.last_image = None

    def fill(self, color):
        try:
            self.fill_color = color
            print("Appearance fill")
            self.surface_loaded = False
            self.dirty = 1
        except TypeError:
            self.parent.window.log("ERROR: color should be a 4-tuple (r, g, b, alpha)")
            raise()

    def register_action(self, action : str, handler, begin = False):
        if not begin:
            self.image_actions.append(action)
        else:
            self.image_actions.insert(0, action)
        self.image_handlers[action] = handler
        self.enabled_image_actions[action] = False

    @property
    def is_textured(self):
        """bool: If True, the image is tiled over the background.
        """
        return self.enabled_image_actions["texture"]

    @is_textured.setter
    def is_textured(self, value):
        if value is True:
            self.enabled_image_actions["upscale"] = False
            self.enabled_image_actions["scale"] = False
            self.enabled_image_actions["texture"] = True
        self.call_image_actions["texture"] = True
        self.dirty = 1


    @property
    def is_upscaled(self):
        """bool: If True, the image will be upscaled remaining aspect-ratio.
        """
        return self.enabled_image_actions["upscale"]

    @is_upscaled.setter
    def is_upscaled(self, value):
        if value is True:
            self.disable_action("scale")
            self.enable_action("upscale")
        else:
            self.disable_action("upscale")

    @property
    def is_rotatable(self):
        """bool: If True, the image will be rotated by parent direction"""
        return self.enabled_image_actions["rotate"]

    @is_rotatable.setter
    def is_rotatable(self, value):
        if value is True:
            self.enable_action("rotate")
        else:
            self.disable_action("rotate")

    @property
    def orientation(self):
        """bool: If True, the image will be rotated by parent orientation before it is rotated.

        This should be used, if image is not pointing to right direction"""
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value

    @property
    def is_flipped(self):
        """bool: Flips the token by 180° degrees.

        This can be used e.g. for bouncing actor at border"""
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
        """ bool: Scales the actor to parent-size withour remaining aspect-ratio."""
        return self.enabled_image_actions["scale"]

    @is_scaled.setter
    def is_scaled(self, value):
        if value is True:
            self.disable_action("upscale")
            self.enable_action("scale")
        else:
            self.disable_action("scale")

    @property
    def text(self):
        """
        Returns the current text
        """
        return self._text

    @text.setter
    def text(self, value):
        """
        Sets the current text
        Args:
            value: A new text as string
        """
        if value == "":
            self._text = ""
            self.disable_action("write_text")
            self.surface_loaded = False
        else:
            self._text = value
            self.enable_action("write_text")
            self.surface_loaded = False

    def add_image(self, path: str) -> int:
        """
        Adds an image to the appearance

        Args:
            path: The path to the image relative to actual directory
            crop: tuple: x,y,width, height

        Returns: The index of the added image.

        """
        alpha = False
        if self.__class__.__name__ != "Background":
            alpha = True
        try:
            _image = ir.ImageRenderer.load_image(path=path, alpha=alpha)
        except FileExistsError:
            raise FileExistsError("File '{0}' does not exist. Check your path to the image.".format(path))
        self.images_list.append(_image)
        self.image_paths.append(path)
        self.dirty = 1
        return len(self.images_list) - 1

    @property
    def image(self) -> pygame.Surface:
        if self.dirty == 1:
            if self.images_list and self.images_list[self._image_index]:
                image = self.images_list[self._image_index] # if there is a image list load image by index
            else: # no image files - Render raw surface
                image = self.load_surface()
            for action in self.image_actions:
                if self.dirty == 1:
                    if self.enabled_image_actions[action]:
                        if action in self.image_handlers.keys():
                            if self.parent.size != (0, 0):
                                    image = self.image_handlers[action](image, parent = self.parent, appearance = self)
                    self.parent.dirty = 1
            for blit_image in self.blit_images:
               image.blit(blit_image[0], blit_image[1] )
            self._image = image
            self.call_image_actions = {key: False for key in self.call_image_actions}
            self.dirty = 0
        return self._image

    def load_surface(self) -> pygame.Surface:
        if not self.surface_loaded:
            image = pygame.Surface(self.parent.size, pygame.SRCALPHA)
            image.fill(self.fill_color)
            image.set_alpha(255)
            self.surface_loaded = True
            self.dirty = 1
            self.raw_surface = image
        return self.raw_surface

    def next_sprite(self):
        """

        Returns: Switches the image of the appearance

        """
        if self.is_animated:
            if self._image_index < len(self.images_list) - 1:
                self._image_index = self._image_index + 1
            else:
                self._image_index = 0
            self.dirty = 1
            self.parent.dirty = 1

    @property
    def is_animated(self):
        """bool: If True, the image will be animated.
        Depends on appearance.animation_speed
        """
        return self._is_animated

    @is_animated.setter
    def is_animated(self, value):
        self._is_animated = value

    def count_pixels_by_color(self, rect, color, threshold=(0, 0, 0, 0)):
        """ Counts the number of pixels of a color under the appearance.

        Args:
            color: The color
            threshold: The allowed deviation from the color splitted into r,g,b and alpha values.

        Returns: The number of matching pixes

        """
        surf = pygame.Surface((rect.width, rect.height))
        surf.blit(self._image, (0, 0), rect)
        return pygame.transform.threshold(dest_surf=None,
                                          set_behavior=0,
                                          surf=surf,
                                          search_color=color,
                                          threshold=threshold)

    def color_at(self, position: board_position.BoardPosition) -> tuple:
        """
        Returns the color at a specific position

        Args:
            position: The position to search for

        Returns: The color

        """
        if type(position) == tuple:
            position = board_position.BoardPosition(position[0],position[1])
        if position.is_on_board():
            return self._image.get_at(position.to_pixel())

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

    def blit(self, path, position: tuple, size: tuple = (0,0) ):
        """
        Blits an image to the background

        Args:
            path: Path to the image
            position: Top left position
            size: Size of blitted image

        Returns:

        """

    def blit(self, path, position: tuple, size: tuple = (0, 0)):
        _blit_image = ir.ImageRenderer.load_image(path=path, alpha=True)
        if size != (0,0):
            _blit_image = pygame.transform.scale(_blit_image, size)
        self.blit_images.append((_blit_image, position, size))

    def colorize(self, color):
        self.color = color
        self.enabled_image_actions["colorize"] = True
        self.call_action("colorize")
