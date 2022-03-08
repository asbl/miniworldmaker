import asyncio
import pygame
import inspect
from collections import defaultdict
from miniworldmaker.appearances.managers import font_manager
from miniworldmaker.appearances.managers import image_manager
from miniworldmaker.appearances.managers import transformations_manager


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
        self._dirty = 0
        self.call_image_actions = {}
        self.raw_image = pygame.Surface((0, 0))  # size set in image()-method
        self._image = pygame.Surface((0, 0))  # size set in image()-method
        self.surface_loaded = False
        self.last_image = None
        self.font_manager = font_manager.FontManager()
        self.image_manager = image_manager.ImageManager(self)
        self.transformations_manager = transformations_manager.TransformationsManager(self)

    def after_init(self):
        # Called in metaclass
        self.reload_transformations_after("all",)
        self.initialized = True

    def reload_transformations_after(self, value):
        self.transformations_manager.reload_transformations_after(value, self)
        self.dirty = 1

    def draw_shape_append(self, shape, arguments):
        self.draw_shapes.append((shape, arguments))
        self.reload_transformations_after("draw_shapes")

    def draw_shape_set(self, shape, arguments):
        self.draw_shapes = [(shape, arguments)]
        self.reload_transformations_after("draw_shapes")

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value
        if self.parent and value == 1:
            self.parent._dirty = 1

    @property
    def image_paths(self):
        return self.image_manager.image_paths
    
    def _reload_image(self):
        if self.dirty == 1:
            self.dirty = 0
            self.image_manager.reset_image_index()
            image = self.image_manager.load_image_by_image_index()
            image = self.transformations_manager.process_transformation_pipeline(image, self)
            self._image = image
            self.transformations_manager.reset_reload_transformations()

    @property
    def image(self) -> pygame.Surface:
        """Performs all actions in image pipeline"""
        self._reload_image()
        return self._image

    def add_image(self, path: str) -> int:
        """Adds an image to the appearance

        Args:
            path (str): Path to the image relative to actual directory

        Returns:
            Index of the created image.
        """
        return self.image_manager.add_image(path)

    def set_image(self, value: int) -> bool:
        """overwritten in subclass
        """
        pass


    def update(self):
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
        self.reload_transformations_after("all",)

    def visible(self):
        self.reload_transformations_after("all",)