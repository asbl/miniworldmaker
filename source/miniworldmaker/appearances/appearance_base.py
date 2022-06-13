import asyncio
from typing import Union, Tuple

import pygame

import miniworldmaker.appearances.managers.font_manager as font_manager
import miniworldmaker.appearances.managers.image_manager as image_manager
import miniworldmaker.appearances.managers.transformations_manager as transformations_manager
import miniworldmaker.tools.binding as binding

from miniworldmaker.exceptions.miniworldmaker_exception import MiniworldMakerError
from miniworldmaker.appearances.managers.image_manager import ImageManager


class MetaAppearance(type):
    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        instance.after_init()
        return instance


class AppearanceBase(metaclass=MetaAppearance):
    counter = 0

    def __init__(self):
        self.id = AppearanceBase.counter + 1
        AppearanceBase.counter += 1
        self.initialized = False
        self.parent = None
        self.board = None
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
        self.image_manager = image_manager.ImageManager(self)
        self.transformations_manager = transformations_manager.TransformationsManager(self)
        self.image_manager.add_default_image()
        # properties
        self.texture_size = (0, 0)
        self.animation_speed = 100  #: The animation speed for animations
        self.loop = False
        self.animation_length = 0
        self.dirty = 1


    def after_init(self):
        # Called in metaclass
        self.reload_transformations_after(
            "all",
        )
        self.initialized = True

    def reload_transformations_after(self, value):
        if hasattr(self, "transformations_manager"):
            self.transformations_manager.reload_transformations_after(value)
            self.dirty = 1

    def draw_shape_append(self, shape, arguments):
        self.draw_shapes.append((shape, arguments))
        self.reload_transformations_after("all")

    def draw_shape_set(self, shape, arguments):
        self.draw_shapes = [(shape, arguments)]
        self.reload_transformations_after("all")

    def draw_image_append(self, surface, rect):
        self.draw_images.append((surface, rect))
        self.reload_transformations_after("all")

    def draw_image_set(self, surface, rect):
        self.draw_images = [(surface, rect)]
        self.reload_transformations_after("all")

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value
        if self.parent and value == 1:
            self.parent.dirty = 1
            
    def _reload_image(self):
        """If dirty, the image will be reloaded.
        The image pipeline will be  processed, defined by "reload_transformations_after"
        """
        if self.dirty == 1:
            self._reload_dirty_image()

    def _reload_dirty_image(self):
        """Reloads image from image_index in image_manager.images_list and processes transformations pipeline
        
        Called by property `image`, if image is dirty
        Sets dirty to 0.
        """
        self.dirty = 0
        image = self.image_manager.load_image_by_image_index()
        image = self.transformations_manager.process_transformation_pipeline(image, self)
        self._image = image

    @property
    def image(self) -> pygame.Surface:
        """Performs all actions in image pipeline"""
        self._reload_image()
        return self._image

    def add_images(self, sources : list):
        assert type(sources) == list
        for image in sources:
            self.add_image(image)
        
    def add_image(self, source: Union[str, Tuple, pygame.Surface]) -> int:
        """Adds an image to the appearance

        Returns:
            Index of the created image.
        """
        if type(source) not in [str, pygame.Surface, tuple]:
            raise MiniworldMakerError(f"Error: Image source has wrong format (expected str or pygame.Surface, got {type(source)}")
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
        asyncio.run(self.image_manager.update())
        return 1

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

    def rotated(self):
        self.reload_transformations_after("rotate")

    def resized(self):
        self.reload_transformations_after(
            "scale",
        )

    def visible(self):
        self.reload_transformations_after(
            "all",
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
            self.dirty = 1
        else:
            self.font_manager.text = value
        self.reload_transformations_after(
            "all",
        )

    @property
    def images(self):
        return self.image_manager.images_list
