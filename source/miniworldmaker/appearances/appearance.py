import asyncio
import inspect
import os
from pathlib import Path
from collections import defaultdict

import nest_asyncio
import pygame
from miniworldmaker.board_positions import board_position, board_position_factory
from miniworldmaker.exceptions.miniworldmaker_exception import ColorException
from miniworldmaker.app import file_manager
from miniworldmaker.tools import binding

class MetaAppearance(type):
    def __call__(cls, *args, **kwargs):
        try:
            instance = super().__call__(*args, **kwargs)
        except TypeError:
            raise TypeError(
                "Wrong number of arguments for {0}-constructor. See method-signature: {0}{1}".format(cls.__name__,
                                                                                                     inspect.signature(
                                                                                                         cls.__init__)))
        instance.after_init()
        return instance


class Appearance(metaclass=MetaAppearance):
    """ Base class of token costumes and board backgrounds

    The class contains all methods and attributes to display and animate images of the objects, render text on the images or display overlays.

    """

    _images_dict = {}  # dict with key: image_path, value: loaded image
    counter = 0

    def __init__(self):
        self.initialized = False
        self.dirty = 0
        self.blit_images = []  # Images which are blitted on the background
        self.parent = None
        self.board = None
        self.images_list = []  # Original images
        self._image_index = 0  # current_image index (for animations)
        self.id = Appearance.counter + 1
        Appearance.counter += 1
        self.image_paths = []  # list with all images
        # properties
        self.raw_image = pygame.Surface((1, 1))  # size set in image()-method
        self._image = pygame.Surface((1, 1))  # size set in image()-method
        self.cached_image = pygame.Surface((1, 1))
        self.call_image_actions = {}
        self.animation_speed = 100  #: The animation speed for animations
        self._is_animated = False
        self.loop = False
        self._is_flipped = False
        self._current_animation_images = None
        self.current_animation = None
        self._is_textured = False
        self._is_upscaled = False
        self._is_scaled = False
        self._is_scaled_to_width = False
        self._is_scaled_to_height = False
        self._is_rotatable = False
        self._flip_vertical = False
        self._orientation = False
        self._text = ""
        self._coloring = None  # Color for colorize operation
        self.draw_shapes = []
        # "Action name", image_action_method, "Attribute", enabled)
        self.image_actions_pipeline = [
            ("orientation", self.image_action_set_orientation, "orientation", False),
            ("draw_shapes", self.image_action_draw_shapes, "draw_shapes", False),
            ("texture", self.image_action_texture, "is_textured", False),
            ("scale", self.image_action_scale, "is_scaled", False),
            ("scale_to_width", self.image_action_scale_to_width, "is_scaled_to_width", False),
            ("scale_to_height", self.image_action_scale_to_height, "is_scaled_to_height", False),
            ("upscale", self.image_action_upscale, "is_upscaled", False),
            ("write_text", self.image_action_write_text, "text", False),
            ("flip", self.image_action_flip, "is_flipped", False),
            ("coloring", self.image_action_coloring, "coloring", False),
            ("rotate", self.image_action_rotate, "is_rotatable", False),
            ("flip_vertical", self.image_action_flip_vertical, "flip_vertical", False),
        ]
        self.fill_color = (0, 0, 255, 255)  #: background_color if actor has no background image
        self.color = (255, 255, 255, 255)  #: color for overlays
        self._font_size = 0  #: font_size if token-text != ""
        self.text_position = (0, 0)  #: Position of text relative to the top-left pixel of token
        self.font_path = None  #: Path to font-file
        self.dirty = 1
        self.reload_actions = defaultdict()
        self.surface_loaded = False
        self.last_image = None
        self.cached_images = defaultdict()
        self.animation_length = 0

    def after_init(self):
        self._reload_all()
        # self.update()
        self.initialized = True

    def _reload_all(self):
        self.dirty = 1
        self.call_action("all")

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        self._font_size = value
        self.call_action("write_text")

    def set_animation_speed(self, value):
        self.animation_speed = value

    @property
    def is_textured(self):
        """
        bool: If True, the image is tiled over the background.

        Examples:
            Defines a textured board

            >>> class MyBoard(TiledBoard):
            >>>    def on_setup(self):
            >>>         self.add_image(path="images/stone.png")
            >>>         self.background.is_textured = True
            >>>         self.background.is_scaled_to_tile = True
            >>>         self.player = Player(position=(3, 4))
        """
        return self._is_textured

    @is_textured.setter
    def is_textured(self, value):
        self._is_textured = value
        self.call_action("texture")

    @property
    def is_upscaled(self):
        """
        bool: If True, the image will be upscaled remaining aspect-ratio.

        Examples:

            >>> class Player(Token):
            >>>    def on_setup(self):
            >>>         self.add_image("background_image.jpg")
            >>>         self.costume.is_upscaled = True

        """
        return self._is_upscaled

    @is_upscaled.setter
    def is_upscaled(self, value):
        self._is_upscaled = value
        self.call_action("upscale")

    @property
    def is_rotatable(self):
        """
        
        Returns:
            If True, the image will be rotated by parent direction

        Examples:

            >>> class Player(Token):
            >>>    def on_setup(self):
            >>>         self.add_image("background_image.jpg")
            >>>         self.costume.is_rotatable = True

        """
        return self._is_rotatable

    @is_rotatable.setter
    def is_rotatable(self, value):
        self._is_rotatable = value
        self.dirty = 1

    @property
    def flip_vertical(self):
        """Flips image vertical
        
        Returns:
            If True, the image will be flipped l/r (e.g. for fighters in a street-fighter like game.

        Examples:

            >>> class Player(Token):
            >>>    def on_setup(self):
            >>>         self.add_image("background_image.jpg")
            >>>         self.costume.flip_vertical = True

        """
        return self._flip_vertical

    @flip_vertical.setter
    def flip_vertical(self, value):
        self._flip_vertical = value
        if self._flip_vertical is True:
            self.is_rotatable = False
        self.dirty = 1

    @property
    def orientation(self):
        """bool: If True, the image will be rotated by parent orientation before it is rotated.

        Examples:

            >>> class Player(Token):
            >>>    def on_setup(self):
            >>>         self.add_image("background_image.jpg")
            >>>         self.costume.orientation = -90
        """
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value
        self.call_action("orientation")

    @property
    def is_flipped(self):
        """bool: Flips the token by 180° degrees.

        This can be used e.g. for bouncing actor at border"""
        return self._is_flipped

    @is_flipped.setter
    def is_flipped(self, value):
        self._is_flipped = value
        self.call_action("flip")

    @property
    def is_scaled(self):
        """ bool: Scales the actor to parent-size withour remaining aspect-ratio."""
        return self._is_scaled

    @is_scaled.setter
    def is_scaled(self, value):
        self._is_scaled = value
        self.call_action("scale")

    @property
    def is_scaled_to_width(self):
        return self._is_scaled_to_width

    @is_scaled_to_width.setter
    def is_scaled_to_width(self, value):
        self.is_scaled = False
        self._is_scaled_to_width = value
        self.call_action("scale_to_width")

    @property
    def is_scaled_to_height(self):
        return self._is_scaled_to_height

    @is_scaled_to_height.setter
    def is_scaled_to_height(self, value):
        self.is_scaled = False
        self._is_scaled_to_height = value
        self.call_action("scale_to_height")

    @property
    def coloring(self):
        """
        Defines a colored layer. Coloring is True or false. The color is defined by the attribute appearance.color

        """
        return self._coloring

    @coloring.setter
    def coloring(self, value):
        self._coloring = value
        self.call_action("coloring")
        self.dirty = 1

    @property
    def text(self):
        """
        Examples:

            >>> explosion = Explosion(position=other.position.up(40).left(40))
            >>> explosion.costume.is_animated = True
            >>> explosion.costume.text_position = (100, 100)
            >>> explosion.costume.text = "100"
        """
        return self._text

    @text.setter
    def text(self, value):
        if value == "":
            self._text = ""
            self.dirty = 1
        else:
            self._text = value
            self.dirty = 1
        # self.call_action("write_text") #@todo: Write text should be sufficient
        self._reload_all()

    def fill(self, color):
        try:
            self.fill_color = color
            self.surface_loaded = False
            self.dirty = 1
        except TypeError:
            raise ColorException("ERROR: color should be a 4-tuple (r, g, b, alpha)")

    def draw_shape_append(self, shape, arguments):
        self.draw_shapes.append((shape, arguments))
        self.call_action("draw_shapes")

    def draw_shape_set(self, shape, arguments):
        self.draw_shapes = [(shape, arguments)]
        self.call_action("draw_shapes")

    def remove_last_image(self):
        del self.images_list[-1]
        self.set_image(-1)
        self._reload_all()

    def find_image_file(self, path: str) -> str:
        """Finds a file by a given relative path (e.g. images/myimage.jpg)
        
        The method tries to correct a path if file ending is missing but image is present.

        Args:
            path (str): path to image, e.g. images/myimage.jpg.

        Returns:
            str: the corrected path
        """        
        canonicalized_path = file_manager.FileManager.relative_to_absolute_path(path)
        if Path(canonicalized_path).is_file():
            return Path(canonicalized_path)
        else:
            if not file_manager.FileManager.has_ending:
                return file_manager.FileManager.get_path_with_file_ending(path, ["jpg", "jpeg", "png"])
            else:
                return file_manager.FileManager.get_path_with_file_ending(canonicalized_path.split(".")[0], ["jpg", "jpeg", "png"])

    @staticmethod
    def load_image(path):
        """
        Loads an image from an path.

        Args:
            path: The path to image

        Returns: 
            The image loaded

        """
        try:
            canonicalized_path = str(path).replace('/', os.sep).replace('\\', os.sep)
            if canonicalized_path in Appearance._images_dict.keys():
                # load image from img_dict
                _image = Appearance._images_dict[canonicalized_path]
            else:
                try:
                    _image = pygame.image.load(canonicalized_path).convert_alpha()
                    Appearance._images_dict[canonicalized_path] = _image
                except pygame.error:
                    raise FileExistsError(
                        "File '{0}' does not exist. Check your path to the image.".format(path))
            return _image
        except FileExistsError:
            raise FileExistsError(
                "File '{0}' does not exist. Check your path to the image.".format(path))

    def add_image(self, path: str) -> int:
        """Adds an image to the appearance

        Args:
            path (str): Path to the image relative to actual directory

        Returns:
            Index of the created image.
        """
        path = self.find_image_file(path)
        # set image by path
        _image = Appearance.load_image(path)
        self.images_list.append(_image)
        self.image_paths.append(path)
        self.dirty = 1
        self._reload_all()
        return len(self.images_list) - 1

    def add_images(self, list_of_paths: list):
        for path in list_of_paths:
            self.add_image(path)

    def blit(self, path, position: tuple, size: tuple = (0, 0)):
        """
        Blits an image to the background

        Args:
            path: Path to the image
            position: Top left position
            size: Size of blitted image

        Returns:

        """
        _blit_image = Appearance.load_image(path)
        if size != (0, 0):
            _blit_image = pygame.transform.scale(_blit_image, size)
        self.image.blit(_blit_image, position)
        self.blit_images.append((_blit_image, position, size))

    @property
    def image(self) -> pygame.Surface:
        return self._image

    def load_surface(self) -> pygame.Surface:
        if not self.surface_loaded:
            image = pygame.Surface((self.parent.width, self.parent.height), pygame.SRCALPHA)
            image.fill(self.fill_color)
            image.set_alpha(255)
            self.dirty = 1
            self.raw_image = image
        return self.raw_image

    def _reset_image_index(self):
        if self._current_animation_images:
            self._image_index = len(self.images_list) - 1


    def _load_image_by_image_index(self):
        if self.images_list and self._image_index < len(self.images_list) and self.images_list[self._image_index]:
            # if there is a image list load image by index
            image = self.images_list[self._image_index]
        else:  # no image files - Render raw surface
            image = self.load_surface()
        return image

    def _perform_action_pipeline_on_image(self, image):
        for img_action in self.image_actions_pipeline:
                # If an image action is to be executed again,
                # load the last cached image from the pipeline and execute
                # all subsequent image actions.
                if self.reload_actions[img_action[0]] is False \
                        and img_action[0] in self.cached_images.keys() \
                        and self.cached_images[img_action[0]]:
                    if getattr(self, img_action[2]) and self.parent.size != (0, 0):
                            image = self.cached_images[img_action[0]]  # Reload image from cache
                else:  # reload_actions is true
                    if getattr(self, img_action[2]) and self.parent.size != (0, 0):
                            # perform image action
                            image = img_action[1](image, parent=self.parent)
                            self.cached_images[img_action[0]] = image
                    self.parent.dirty = 1
        return image

    def _blit_on_image(self, image):
        for blit_image in self.blit_images:
                image.blit(blit_image[0], blit_image[1])

        return image


    def reload_image(self):
        """ Performs all actions in image pipeline"""
        if self.dirty == 1:
            self._reset_image_index()
            image = self._load_image_by_image_index()
            image = self._perform_action_pipeline_on_image(image)
            image = self._blit_on_image(image)
            self._image = image
            self.dirty = 0
            for key in self.reload_actions.keys():
                self.reload_actions[key] = False
        return self.image

    async def next_image(self):
        """
        Switches to the next image of the appearance.
        """
        if self.is_animated:
            if self._image_index < len(self.images_list) - 1:
                self._image_index = self._image_index + 1
            else:
                if not self.loop:
                    self.is_animated = False
                    self.after_animation()
                self._image_index = 0
            self.dirty = 1
            self.parent.dirty = 1
            self._reload_all()

    async def first_image(self):
        """
        Switches to the first image of the appearance.
        """
        self._image_index = 0
        self.dirty = 1
        self.parent.dirty = 1
        self._reload_all()

    def set_image(self, value: int) -> bool:
        if value == -1:
            value = len(self.images_list) - 1
        if 0 <= value < len(self.images_list):
            self._image_index = value
            self.dirty = 1
            self.parent.dirty = 1
            self._reload_all()
            return True
        else:
            return False

    def update(self):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self._update())
        nest_asyncio.apply()
        loop.run_until_complete(task)
        return 1

    async def _update(self):
        """ 
        method is overwritten in subclasses costume and background.
        """
        pass

    @property
    def is_animated(self):
        """bool: If True, the image will be animated.
        Depends on appearance.animation_speed

        Examples:

            >>> class Robot(Token):
            >>>
            >>> def __init__(self, position):
            >>>     super().__init__(position)
            >>>     self.add_image("images/robot_blue1.png")
            >>>     self.add_image("images/robot_blue2.png")
            >>>     self.size = (99, 99)
            >>>     self.costume.animation_speed = 30
            >>>     self.costume.is_animated = True
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

    def get_color_from_pixel(self, position: board_position.BoardPosition) -> tuple:
        """
        Returns the color at a specific position

        Args:
            position: The position to search for

        Returns: The color

        """
        position = board_position_factory.BoardPositionFactory(self).create(position)
        return self._image.get_at(position.to_int())

    def call_action(self, action):
        reload = False
        for img_action in self.image_actions_pipeline:
            if img_action[0] == action or action == "all":
                reload = True  # reload image action
            if reload:
                self.reload_actions[img_action[0]] = True  # reload all actions after image action
        self.dirty = 1
        self.parent.dirty = 1
        # self.update()

    def call_actions(self, actions):
        reload = False
        for img_action in self.image_actions_pipeline:
            if img_action[0] in actions:
                reload = True
            if reload:
                self.reload_actions[img_action[0]] = True
        self.dirty = 1
        self.parent.dirty = 1
        return self.image

    def call_all_actions(self):
        self.call_action("all")

    def image_action_draw_shapes(self, image: pygame.Surface, parent) -> pygame.Surface:
        for draw_action in self.draw_shapes:
            draw_action[0](image, *draw_action[1])
        return image

    def image_action_texture(self, image, parent):
        background = pygame.Surface((self.parent.width, self.parent.height))
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
            scale_factor_x = parent.width / image.get_width()
            scale_factor_y = parent.height / image.get_height()
            scale_factor = min(scale_factor_x, scale_factor_y)
            new_width = int(image.get_width() * scale_factor)
            new_height = int(image.get_height() * scale_factor)
            image = pygame.transform.scale(image, (new_width, new_height))
        return image

    def image_action_scale(self, image: pygame.Surface, parent, ) -> pygame.Surface:
        image = pygame.transform.scale(image, (self.parent.width, self.parent.height))
        return image

    def image_action_scale_to_height(self, image: pygame.Surface, parent, ) -> pygame.Surface:
        scale_factor = parent.height / image.get_height()
        new_width = int(image.get_width() * scale_factor)
        new_height = int(image.get_height() * scale_factor)
        image = pygame.transform.scale(image, (new_width, new_height))
        return image

    def image_action_scale_to_width(self, image: pygame.Surface, parent, ) -> pygame.Surface:
        scale_factor = parent.width / image.get_width()
        new_width = int(image.get_width() * scale_factor)
        new_height = int(image.get_height() * scale_factor)
        image = pygame.transform.scale(image, (new_width, new_height))
        return image

    def image_action_rotate(self, image: pygame.Surface, parent) -> pygame.Surface:
        if self.parent.direction != 0:
            rotated_image = pygame.transform.rotozoom(image, - (self.parent.direction), 1)
            #image.blit(rotated_image, new_rect)
            return rotated_image
        else:
            return image

    def image_action_flip_vertical(self, image: pygame.Surface, parent) -> pygame.Surface:
        if self.parent.direction < 0:
            return pygame.transform.flip(image, True, False)
        else:
            return image

    def image_action_set_orientation(self, image: pygame.Surface, parent) -> pygame.Surface:
        if self.parent.orientation != 0:
            return pygame.transform.rotate(image, - self.parent.orientation)
        else:
            return image

    def image_action_flip(self, image: pygame.Surface, parent) -> pygame.Surface:
        return pygame.transform.flip(image, self.is_flipped, False)

    def image_action_coloring(self, image: pygame.Surface, parent) -> pygame.Surface:
        """
        Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
        original).

        :param image: Surface to create a colorized copy of
        :param newColor: RGB color to use (original alpha values are preserved)
        :return: New colorized Surface instance
        """
        image = image.copy()
        # zero out RGB values
        image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)  # Fill black
        # add in new RGB values
        new_color = self.color[0:3] + (0,)
        image.fill(new_color, None, pygame.BLEND_RGBA_ADD)  # Add color
        new_color = (255, 255, 255) + (self.color[3],)
        image.fill(new_color, None, pygame.BLEND_RGBA_MULT)  # Multiply transparency
        return image

    @staticmethod
    def crop_image(self, image: pygame.Surface, parent, appearance) -> pygame.Surface:
        cropped_surface = pygame.Surface((self.parent.width, self.parent.height))
        cropped_surface.fill((255, 255, 255))
        cropped_surface.blit(image, (0, 0), (0, 0, (self.parent.width, self.parent.height)))
        return cropped_surface

    def image_action_write_text(self, image: pygame.Surface, parent) -> pygame.Surface:
        font_size = 0
        if self.font_size == 0:
            font_size = parent.width
        else:
            font_size = self.font_size
        if self.font_path is None:
            my_font = pygame.font.SysFont("monospace", font_size)
        else:
            my_font = pygame.font.Font(self.font_path, font_size)
        label = my_font.render(self.text, 1, self.color)
        image.blit(label, self.text_position)
        return image

    def set_font(self, font, font_size):
        self.font_path = font
        self.font_size = font_size

    def animate(self):
        self.is_animated = True

    def after_animation(self):
        """
        the method is overwritten in subclasses costume and appearance
        """
        pass


    def register(self, method: callable):
        """ 
        Register method for decorator. Registers method to token or background.
        """        
        bound_method = binding.bind_method(self, method)
        return bound_method
        
