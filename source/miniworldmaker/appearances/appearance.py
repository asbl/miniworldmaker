import pygame
from miniworldmaker.board_positions import board_position, board_position_factory
from miniworldmaker.exceptions.miniworldmaker_exception import ColorException
from miniworldmaker.tools import binding
from miniworldmaker.appearances import appearance_base


class Appearance(appearance_base.AppearanceBase):
    """Base class of token costumes and board backgrounds

    The class contains all methods and attributes to display and animate images of the objects, render text on the images or display overlays.

    """

    def __init__(self):
        super().__init__()
        # properties
        self._is_flipped = False
        self._is_animated = False
        self._is_textured = False
        self._is_upscaled = False
        self._is_scaled = False
        self._is_scaled_to_width = False
        self._is_scaled_to_height = False
        self._is_rotatable = False
        self._flip_vertical = False
        self._orientation = False
        self.animation_speed = 100  #: The animation speed for animations
        self.loop = False
        self._coloring = None  # Color for colorize operation
        # "Action name", transformation_method, "Attribute", enabled)
        self._transparency = False
        self._alpha = 255
        self.fill_color = (0, 0, 255, 255)  #: background_color if actor has no background image
        self.color = (255, 255, 255, 255)  #: color for overlays
        self.dirty = 1
        self.animation_length = 0

    @property
    def font_size(self):
        return self.font_manager.font_size

    @font_size.setter
    def font_size(self, value):
        self.font_manager.font_size = value
        self.reload_transformations_after("write_text")

    def set_font(self, font, font_size):
        self.font_manager.font_path = font
        self.font_manager.font_size = font_size

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
        self.reload_transformations_after("texture")

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
        self.reload_transformations_after("upscale")

    @property
    def is_rotatable(self):
        """Is appearance rotatable?

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
        self.reload_transformations_after("orientation")

    @property
    def is_flipped(self):
        """bool: Flips the token by 180° degrees.

        This can be used e.g. for bouncing actor at border"""
        return self._is_flipped

    @is_flipped.setter
    def is_flipped(self, value):
        self._is_flipped = value
        self.reload_transformations_after("flip")

    @property
    def is_scaled(self):
        """bool: Scales the actor to parent-size withour remaining aspect-ratio."""
        return self._is_scaled

    @is_scaled.setter
    def is_scaled(self, value):
        self._is_scaled = value
        self.reload_transformations_after("scale")

    @property
    def is_scaled_to_width(self):
        return self._is_scaled_to_width

    @is_scaled_to_width.setter
    def is_scaled_to_width(self, value):
        self.is_scaled = False
        self._is_scaled_to_width = value
        self.reload_transformations_after("scale_to_width")

    @property
    def is_scaled_to_height(self):
        return self._is_scaled_to_height

    @is_scaled_to_height.setter
    def is_scaled_to_height(self, value):
        self.is_scaled = False
        self._is_scaled_to_height = value
        self.reload_transformations_after("scale_to_height")

    @property
    def coloring(self):
        """
        Defines a colored layer. Coloring is True or false. The color is defined by the attribute appearance.color

        """
        return self._coloring

    @coloring.setter
    def coloring(self, value):
        self._coloring = value
        self.reload_transformations_after("coloring")

    @property
    def transparency(self):
        """
        Defines a transparency. Coloring is True or false. The color is defined by the attribute appearance.alpha

        """
        return self._transparency

    @transparency.setter
    def transparency(self, value):
        self._transparency = value
        self.reload_transformations_after("transparency")

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = value
        if value == 255:
            self.transparency = False
        else:
            self.transparency = True

    @property
    def text(self):
        """
        Examples:

            >>> explosion = Explosion(position=other.position.up(40).left(40))
            >>> explosion.costume.is_animated = True
            >>> explosion.costume.text_position = (100, 100)
            >>> explosion.costume.text = "100"
        """
        return self.font_manager.text

    @text.setter
    def text(self, value):
        if value == "":
            self.font_manager.text = ""
            self.dirty = 1
        else:
            self.font_manager.text = value
            self.dirty = 1
        self._reload_all()

    def get_text_width(self):
        return self.font_manager.get_font_width()

    def fill(self, color):
        try:
            self.fill_color = color
            self.surface_loaded = False
            self.dirty = 1
        except TypeError:
            raise ColorException("ERROR: color should be a 4-tuple (r, g, b, alpha)")

    def remove_last_image(self):
        del self.animation_manager.images_list[-1]
        self.set_image(-1)
        self.reload_transformations_after("all")

    def add_image(self, path: str) -> int:
        """Adds an image to the appearance

        Args:
            path (str): Path to the image relative to actual directory

        Returns:
            Index of the created image.
        """
        super().add_image(path)

    def add_images(self, list_of_paths: list):
        for path in list_of_paths:
            self.add_image(path)

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
        """Counts the number of pixels of a color under the appearance.

        Args:
            color: The color
            threshold: The allowed deviation from the color splitted into r,g,b and alpha values.

        Returns: The number of matching pixes

        """
        surf = pygame.Surface((rect.width, rect.height))
        surf.blit(self._image, (0, 0), rect)
        return pygame.transform.threshold(
            dest_surf=None, set_behavior=0, surf=surf, search_color=color, threshold=threshold
        )

    def get_color_from_pixel(self, position: board_position.BoardPosition) -> tuple:
        """
        Returns the color at a specific position

        Args:
            position: The position to search for

        Returns: The color

        """
        position = board_position_factory.BoardPositionFactory(self).create(position)
        return self._image.get_at(position.to_int())

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

    def reset(self):
        self.animation_manager.set_image_index(0)
        self.animation_manager.end_animation(self)
