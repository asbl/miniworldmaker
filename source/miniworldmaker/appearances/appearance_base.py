from typing import Union, Tuple

import pygame

import miniworldmaker.appearances.managers.font_manager as font_manager
import miniworldmaker.appearances.managers.image_manager as image_manager
import miniworldmaker.appearances.managers.transformations_manager as transformations_manager
import miniworldmaker.tools.binding as binding

from miniworldmaker.exceptions.miniworldmaker_exception import MiniworldMakerError
from miniworldmaker.appearances.managers.image_manager import ImageManager
from miniworldmaker.boards import board
from abc import ABC

class MetaAppearance(type, ABC):
    def __call__(cls, *args, **kwargs):
        instance = type.__call__(cls, *args, **kwargs)  # create a new Appearance of type...
        instance.after_init()
        return instance


class AppearanceBase(metaclass=MetaAppearance):
    counter = 0

    RELOAD_ACTUAL_IMAGE = 1
    LOAD_NEW_IMAGE = 2

    def __init__(self):
        self.id = AppearanceBase.counter + 1
        AppearanceBase.counter += 1
        self.initialized = False
        self._flag_transformation_pipeline = False
        self.parent = None
        self.draw_shapes = []
        self.draw_images = []
        self._is_flipped = False
        self._is_animated = False
        self._is_textured = False
        self._is_centered = True
        self._is_upscaled = False
        self._is_scaled = False
        self._is_scaled_to_width = False
        self._is_scaled_to_height = False
        self._is_rotatable = False
        self._orientation = False
        self._coloring = None  # Color for colorize operation
        self._transparency = False
        self._border = 0
        self._is_filled = False
        self._fill_color = (255, 0, 255, 100)
        self._border_color = None
        self._alpha = 255
        self._dirty = 0
        self._image = pygame.Surface((0, 0))  # size set in image()-method
        self.surface_loaded = False
        self.last_image = None
        self.font_manager = font_manager.FontManager(self)
        self.image_manager : "image_manager.ImageManager" = image_manager.ImageManager(self)
        self.transformations_manager = transformations_manager.TransformationsManager(self)
        self.image_manager.add_default_image()
        # properties
        self.texture_size = (0, 0)
        self.animation_speed = 10  #: The animation speed for animations
        self.loop = False
        self.animation_length = 0
        self._animation_start_frame = 0
        
    @property
    def board(self) -> "board.Board":
        return None

    def after_init(self):
        # Called in metaclass
        self.set_dirty("all", AppearanceBase.LOAD_NEW_IMAGE)
        self.initialized = True

    def draw_shape_append(self, shape, arguments):
        self.draw_shapes.append((shape, arguments))

    def draw_shape_set(self, shape, arguments):
        self.draw_shapes = [(shape, arguments)]

    def draw_image_append(self, surface, rect):
        self.draw_images.append((surface, rect))

    def draw_image_set(self, surface, rect):
        self.draw_images = [(surface, rect)]

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        if value == 0:
            self._dirty = 0
        else:
            self.set_dirty(value)

    def set_dirty(self, value="all", status=1):
        if hasattr(self, "transformations_manager"):
            if value != None:
                self.transformations_manager.flag_reload_actions_for_transformation_pipeline(value)
            if status >= self._dirty:
                self._dirty = status
            if self.parent:
                self.parent.dirty = 1

    @property
    def image(self) -> pygame.Surface:
        """Performs all actions in image pipeline"""
        return self.get_image()
    
    def get_image(self):
        """If dirty, the image will be reloaded.
        The image pipeline will be  processed, defined by "set_dirty"
        """
        if self.dirty >= self.RELOAD_ACTUAL_IMAGE or not self._image and not self._flag_transformation_pipeline:
            dirty = self.dirty
            self.dirty = 0
            self._flag_transformation_pipeline = True
            self._before_transformation_pipeline()
            image = self.image
            if dirty >= self.RELOAD_ACTUAL_IMAGE:
                # @todo: Not working: Replace RELOAD_ACTUAL_IMAGE with LOAD NEW IMAGE
                image = self.image_manager.load_image_from_image_index()
            if dirty >= self.RELOAD_ACTUAL_IMAGE:
                image = self.transformations_manager.process_transformation_pipeline(image, self)
                self._after_transformation_pipeline()
                self._flag_transformation_pipeline = False
            self._image = image
        return self._image

    def _before_transformation_pipeline(self):
        pass
    def _after_transformation_pipeline(self):
        pass


    def add_images(self, sources: list):
        assert type(sources) == list
        for image in sources:
            self.add_image(image)

    def add_image(self, source: Union[str, Tuple, pygame.Surface]) -> int:
        """Adds an image to the appearance

        Returns:
            Index of the created image.
        """
        if type(source) not in [str, pygame.Surface, tuple]:
            raise MiniworldMakerError(
                f"Error: Image source has wrong format (expected str or pygame.Surface, got {type(source)}"
            )
        self.image_manager.add_image(source)

    def set_image(self, source: Union[int, "AppearanceBase"]) -> bool:
        if type(source) == int:
            return self.image_manager.set_image_index(source)
        elif type(source) == tuple:
            surface = image_manager.ImageManager.get_surface_from_color(source)
            self.image_manager.replace_image(surface, ImageManager.COLOR, source)

    def update(self):
        """Loads the next image,
        called 1/frame"""
        self._load_image()
        return 1

    def _load_image(self):
        """Loads the image,
        
        * switches image if neccessary
        * processes transformations pipeline if neccessary
        """
        if self.is_animated and self._animation_start_frame != self.board.frame:
            if self.board.frame != 0 and self.board.frame % self.animation_speed == 0:
                self.image_manager.next_image()
        self.get_image()


    def __str__(self):
        return (
            self.__class__.__name__
            + "with ID ["
            + str(self.id)
            + "] for parent:["
            + str(self.parent)
            + "], images: "
            + str(self.image_manager.images_list)
        )

    def register(self, method: callable):
        """
        Register method for decorator. Registers method to token or background.
        """
        bound_method = binding.bind_method(self, method)
        return bound_method

    @property
    def text(self):
        """
        Examples:

            .. code-block:: python

                explosion = Explosion(position=other.position.up(40).left(40))
                explosion.costume.is_animated = True
                explosion.costume.text_position = (100, 100)
                explosion.costume.text = "100"
        """
        return self.font_manager.text

    @text.setter
    def text(self, value):
        if value == "":
            self.font_manager.text = ""
            self.set_dirty("write_text", AppearanceBase.RELOAD_ACTUAL_IMAGE)
        else:
            self.font_manager.text = value
        self.set_dirty("write_text",AppearanceBase.RELOAD_ACTUAL_IMAGE)

    @property
    def images(self):
        return self.image_manager.images_list