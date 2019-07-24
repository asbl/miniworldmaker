import pygame
from miniworldmaker.boards import board_position


class Appearance:
    """ Base class of token costumes and board backgrounds

    Die Klasse enthält alle Methoden und Attribute um Bilder der Objekte anzuzeigen, zu animieren, Text auf den Bildern zu rendern  oder Overlays anzuzeigen.

    """

    _images_dict = {}  # dict with key: image_path, value: loaded image

    def __init__(self):
        self.dirty = 0
        self.blit_images = []  # Images which are blitted on the background
        self.parent = None
        self.images_list = []  # Original images
        self._image_index = 0  # current_image index (for animations)
        self.image_paths = []  # list with all images
        # properties
        self.raw_image = pygame.Surface((1, 1))  # size set in image()-method
        self._image = pygame.Surface((1, 1))  # size set in image()-method
        self.cached_image = pygame.Surface((1, 1))
        self.call_image_actions = {}
        self.alpha = True
        self.animation_speed = 60  #: The animation speed for animations
        self._is_animated = False
        self._is_flipped = False
        self._is_textured = False
        self._is_upscaled = False
        self._is_scaled = False
        self._is_rotatable = False
        self._orientation = False
        self._text = ""
        self._coloring = None  # Color for colorize operation
        self.draw_shapes = []
        self.image_preprocess_pipeline = [("orientation", self.image_action_set_orientation, "orientation", None), ]
        self.image_actions_pipeline = [("texture", self.image_action_texture, "is_textured", False),
                                       ("write_text", self.image_action_write_text, "text", False),
                                       ("scale", self.image_action_scale, "is_scaled", False),
                                       ("upscale", self.image_action_upscale, "is_upscaled", False),
                                       ("draw_shapes", self.image_action_draw_shapes, "draw_shapes", False),
                                       ("flip", self.image_action_flip, "is_flipped", False),
                                       ("colorize", self.image_action_color_mixture, "coloring", False),
                                       ("rotate", self.image_action_rotate, "is_rotatable", False),
                                       ]
        self.fill_color = (0, 0, 255, 255)  #: background_color if actor has no background image

        self.color = (255, 255, 255, 255)  #: color for overlays
        self.font_size = 0  #: font_size if token-text != ""
        self.text_position = (0, 0)  #: Position of text relative to the top-left pixel of token
        self.font_path = None  #: Path to font-file
        self.dirty = 1
        self.surface_loaded = False
        self.last_image = None
        self.preprocessed = dict()

    @property
    def is_textured(self):
        """bool: If True, the image is tiled over the background.
        """
        return self._is_textured

    @is_textured.setter
    def is_textured(self, value):
        self._is_textured = value
        self.dirty = 1

    @property
    def is_upscaled(self):
        """bool: If True, the image will be upscaled remaining aspect-ratio.
        """
        return self._is_upscaled

    @is_upscaled.setter
    def is_upscaled(self, value):
        self._is_upscaled = value
        self.dirty = 1

    @property
    def is_rotatable(self):
        """bool: If True, the image will be rotated by parent direction"""
        return self._is_rotatable

    @is_rotatable.setter
    def is_rotatable(self, value):
        self._is_rotatable = value
        self.dirty = 1

    @property
    def orientation(self):
        """bool: If True, the image will be rotated by parent orientation before it is rotated.

        This should be used, if image is not pointing to right direction"""
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value
        if self.orientation != self.parent._orientation:
            self.parent.orientation = self._orientation
        self.preprocessed[self._image_index] = False
        self.dirty = 1

    @property
    def is_flipped(self):
        """bool: Flips the token by 180° degrees.

        This can be used e.g. for bouncing actor at border"""
        return self._is_flipped

    @is_flipped.setter
    def is_flipped(self, value):
        self._is_flipped = value
        self.dirty = 1

    @property
    def is_scaled(self):
        """ bool: Scales the actor to parent-size withour remaining aspect-ratio."""
        return self._is_scaled

    @is_scaled.setter
    def is_scaled(self, value):
        self._is_scaled = value
        self.dirty = 1

    @property
    def coloring(self):
        return self._coloring

    @coloring.setter
    def coloring(self, color):
        self._coloring = color
        self.dirty = 1

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
            self.surface_loaded = False
            self.dirty = 1
        else:
            self._text = value
            self.surface_loaded = False
            self.dirty = 1

    def fill(self, color):
        try:
            self.fill_color = color
            self.surface_loaded = False
            self.dirty = 1
        except TypeError:
            self.parent.window.log("ERROR: color should be a 4-tuple (r, g, b, alpha)")
            raise ()

    def draw_shape_append(self, shape, arguments):
        self.draw_shapes.append((shape, arguments))
        self.dirty = 1

    def draw_shape_set(self, shape, arguments):
        self.draw_shapes = [(shape, arguments)]
        self.dirty = 1

    def add_image(self, path: str) -> int:
        """
        Adds an image to the appearance

        Args:
            path: The path to the image relative to actual directory
            crop: tuple: x,y,width, height

        Returns: The index of the added image.

        """
        _image = Appearance.load_image(path, self.alpha)
        Appearance._images_dict[path] = _image
        self.images_list.append(_image)
        self.image_paths.append(path)
        self._image = self.image
        self.dirty = 1
        return len(self.images_list) - 1

    @staticmethod
    def load_image(path, alpha):
        try:
            if path in Appearance._images_dict.keys():
                # load image from img_dict
                _image = Appearance._images_dict[path]
            else:
                # create new image and add to img_dict
                if not alpha:
                    try:
                        _image = pygame.image.load(path).convert()
                    except pygame.error:
                        raise FileExistsError("File '{0}' does not exist. Check your path to the image.".format(path))
                else:
                    try:
                        _image = pygame.image.load(path).convert_alpha()
                    except pygame.error:
                        raise FileExistsError("File '{0}' does not exist. Check your path to the image.".format(path))
            return _image
        except FileExistsError:
            raise FileExistsError("File '{0}' does not exist. Check your path to the image.".format(path))

    def blit(self, path, position: tuple, size: tuple = (0, 0)):
        """
        Blits an image to the background

        Args:
            path: Path to the image
            position: Top left position
            size: Size of blitted image

        Returns:

        """
        _blit_image = Appearance.load_image(path, True)
        if size != (0, 0):
            _blit_image = pygame.transform.scale(_blit_image, size)
        self.image.blit(_blit_image, position)
        self.blit_images.append((_blit_image, position, size))

    @property
    def image(self) -> pygame.Surface:
        if self.dirty == 1:
            if self.images_list and self.images_list[self._image_index]:
                image = self.images_list[self._image_index]  # if there is a image list load image by index
                if not self._image_index in self.preprocessed.keys() or not self.preprocessed[self._image_index]:
                    for action in self.image_preprocess_pipeline:
                        if getattr(self, action[2]):
                            image = action[1](image, parent=self.parent)
                    self.images_list[self._image_index] = image
                    self.preprocessed[self._image_index] = True
            else:  # no image files - Render raw surface
                image = self.load_surface()
            for action in self.image_actions_pipeline:
                if self.dirty == 1:
                    if getattr(self, action[2]):
                        if self.parent.size != (0, 0):
                            image = action[1](image, parent=self.parent)
                    self.parent.dirty = 1
            for blit_image in self.blit_images:
                image.blit(blit_image[0], blit_image[1])
            self._image = image
            self.dirty = 0
        return self._image

    def load_surface(self) -> pygame.Surface:
        if not self.surface_loaded:
            image = pygame.Surface(self.parent.size, pygame.SRCALPHA)
            image.fill(self.fill_color)
            image.set_alpha(255)
            self.dirty = 1
            self.raw_image = image
        return self.raw_image

    def next_image(self):
        """
        Switches to the next image of the appearance.
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
            position = board_position.BoardPosition(position[0], position[1])
        if position.is_on_board():
            return self._image.get_at(position.to_pixel())

    def changed_all(self):
        self.call_image_actions = {key: True for key in self.call_image_actions}
        self.dirty = 1

    def call_action(self, action):
        self.call_image_actions[action] = True
        self.dirty = 1
        self.parent.dirty = 1

    def image_action_texture(self, image, parent):
        background = pygame.Surface(parent.size)
        background.fill((255, 255, 255))
        i, j, width, height = 0, 0, 0, 0
        while width < parent.width:
            while height < parent.height:
                width = i * image.get_width()
                height = j * image.get_height()
                j += 1
                background.blit(image, (width, height))
            j, height = 0, 0
            i += 1
        return background

    def image_action_upscale(self, image: pygame.Surface, parent) -> pygame.Surface:
        if parent.size != 0:
            scale_factor_x = parent.size[0] / image.get_width()
            scale_factor_y = parent.size[1] / image.get_height()
            scale_factor = min(scale_factor_x, scale_factor_y)
            new_width = int(image.get_width() * scale_factor)
            new_height = int(image.get_height() * scale_factor)
            image = pygame.transform.scale(image, (new_width, new_height))
        return image

    def image_action_scale(self, image: pygame.Surface, parent, ) -> pygame.Surface:
        image = pygame.transform.scale(image, parent.size)
        return image

    def image_action_rotate(self, image: pygame.Surface, parent) -> pygame.Surface:
        if self.parent.direction != 0:
            return pygame.transform.rotate(image, - (self.parent.direction))
        else:
            return image

    def image_action_set_orientation(self, image: pygame.Surface, parent) -> pygame.Surface:
        if self.parent.orientation != 0:
            return pygame.transform.rotate(image, - self.parent.orientation)
        else:
            return image

    def image_action_flip(self, image: pygame.Surface, parent) -> pygame.Surface:
        return pygame.transform.flip(image, self.is_flipped, False)

    def image_action_color_mixture(self, image: pygame.Surface, parent) -> pygame.Surface:
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
        image.fill(self.coloring[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
        return image

    @staticmethod
    def crop_image(image: pygame.Surface, parent, appearance) -> pygame.Surface:
        cropped_surface = pygame.Surface(parent.size)
        cropped_surface.fill((255, 255, 255))
        cropped_surface.blit(image, (0, 0), (0, 0, parent.size[0], parent.size[1]))
        return cropped_surface

    def image_action_write_text(self, image: pygame.Surface, parent) -> pygame.Surface:
        if self.font_path is None:
            if self.font_size == 0:
                font_size = parent.size[1]
            else:
                font_size = self.font_size
            my_font = pygame.font.SysFont("monospace", font_size)
        else:
            my_font = pygame.font.Font(self.font_path)
        label = my_font.render(self.text, 1, self.color)
        image.blit(label, self.text_position)
        return image

    def image_action_draw_shapes(self, image: pygame.Surface, parent) -> pygame.Surface:
        for draw_action in self.draw_shapes:
            draw_action[0](image, *draw_action[1])
            pass
        return image
