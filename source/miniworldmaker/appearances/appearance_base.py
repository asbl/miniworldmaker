import asyncio
import pygame
import inspect
from collections import defaultdict
from miniworldmaker.appearances.managers import font_manager
from miniworldmaker.appearances.managers import image_manager
from miniworldmaker.appearances.managers import animation_manager
from miniworldmaker.appearances.managers import transformations_manager


class MetaAppearance(type):
    def __call__(cls, *args, **kwargs):
        try:
            instance = super().__call__(*args, **kwargs)
        except TypeError:
            raise TypeError(
                "Wrong number of arguments for {0}-constructor. See method-signature: {0}{1}".format(
                    cls.__name__, inspect.signature(cls.__init__)
                )
            )
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
        self.image_manager = image_manager.ImageManager()
        self.animation_manager = animation_manager.AnimationManager()
        self.transformations_manager = transformations_manager.TransformationsManager(self)

    def after_init(self):
        # Called in metaclass
        self._reload_all()
        self.initialized = True

    def _reload_all(self):
        self.reload_transformations_after("all")

    def reload_transformations_after(self, value):
        self.transformations_manager.reload_transformations_after(value)
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
        return self.animation_manager.image_paths
    
    def _reload_image(self):
        if self.dirty == 1:
            self.dirty = 0
            self.animation_manager.reset_image_index()
            image = self.animation_manager.load_image_by_image_index(self)
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
        return self.image_manager.add_image(path, self)

    def set_image(self, value: int) -> bool:
        return self.animation_manager.set_image_index(value, self)


    def update(self):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.animation_manager.update(self))
        loop.run_until_complete(task)
        return 1

    def __str__(self):
        return (
            self.__class__.__name__
            + "with ID ["
            + str(self.id)
            + "] for parent:["
            + str(self.parent)
            + "], images: "
            + str(self.animation_manager.images_list)
        )
