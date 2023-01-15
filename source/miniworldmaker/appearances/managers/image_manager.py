import os
from pathlib import Path
from typing import List, Union, Tuple, Dict

import pygame

import miniworldmaker.base.file_manager as file_manager
from miniworldmaker.exceptions.miniworldmaker_exception import ImageIndexNotExistsError
from miniworldmaker.exceptions.miniworldmaker_exception import MiniworldMakerError


class ImageManager:
    """Handles loading and caching of images."""

    _images_dict = {}  # dict with key: image_path, value: loaded image

    IMAGE_FOLDER = "./images/"
    # types
    IMAGE = 1
    COLOR = 2
    SURFACE = 3

    def __init__(self, appearance):
        self.animation_frame = 0
        self.current_animation_images = None
        self.image_index = 0  # current_image index (for animations) in self.image_lists
        self.images_list: List[Dict] = []  # Original images - remove or add image surfaces here
        self.appearance = appearance
        self.has_image = False
        self.add_default_image()

    @staticmethod
    def load_image(path):
        """
        Loads an image from a path.

        Args:
            path: The path to image

        Returns:
            The image loaded

        """
        try:
            canonical_path = str(path).replace("/", os.sep).replace("\\", os.sep)
            if canonical_path in ImageManager._images_dict.keys():
                # load image from img_dict
                _image = ImageManager._images_dict[canonical_path]
            else:
                try:
                    _image = pygame.image.load(canonical_path).convert_alpha()
                    ImageManager._images_dict[canonical_path] = _image
                except pygame.error:
                    raise FileExistsError("File '{0}' does not exist. Check your path to the image.".format(path))
            return _image
        except FileExistsError:
            raise FileExistsError("File '{0}' does not exist. Check your path to the image.".format(path))

    def find_image_file(self, path: str) -> str:
        """Finds a file by a given relative path (e.g. images/myimage.jpg)

        The method tries to correct a path if file ending is missing but image is present.

        Args:
            path (str): path to image, e.g. images/myimage.jpg.

        Returns:
            str: the corrected path
        """
        return file_manager.FileManager.get_image_path(path)

    @staticmethod
    def cache_images_in_image_folder():
        """is called on program start.
        Loads all images in folder path/images
        """
        jpgs = list(Path(ImageManager.IMAGE_FOLDER).rglob("*.[jJ][pP][gG]"))
        jpegs = list(Path(ImageManager.IMAGE_FOLDER).rglob("*.[jJ][pP][eE][gG]"))
        pngs = list(Path(ImageManager.IMAGE_FOLDER).rglob("*.[pP][nN][gG]"))
        images = jpgs + jpegs + pngs
        for img_path in images:
            ImageManager.load_image(img_path)

    def add_first_image(self, source):
        if len(self.images_list) == 1:
            image = self.images_list.pop(0)
            del image
        self._add_scaling(source)
        self.add_image_from_source(source)

    def add_default_image(self):
        """called in init"""
        if not self.has_image and len(self.images_list) == 0:
            self.appearance.is_scaled = True
            surf = pygame.Surface((1, 1), pygame.SRCALPHA)
            surf.fill(self.appearance.fill_color)
            self.images_list.append({"image": surf, "type": ImageManager.COLOR})
            self.appearance.set_dirty("all", self.appearance.LOAD_NEW_IMAGE)
            return len(self.images_list) - 1

    def add_image(self, source: Union[str, pygame.Surface, Tuple]) -> int:
        """Adds an image to the appearance

        Args:
            source (str): Path to the image relative to actual directory

        Returns:
            Index of the created image.
        """
        if not self.has_image and source:
            self.add_first_image(source)
            self.has_image = True
        elif source:
            return self.add_image_from_source(source)
        else:
            raise MiniworldMakerError("unexpected behaviour")

    def add_image_from_source(self, source: Union[str, list, pygame.Surface, tuple]):
        if type(source) == str:
            return self.add_image_from_path(source)
        elif type(source) == list:
            return self.add_image_from_paths(source)
        elif type(source) == pygame.Surface:
            return self.add_image_from_surface(source)
        elif type(source) == tuple:
            return self.add_image_from_color(source)

    def _add_scaling(self, source: Union[str, list, pygame.Surface, tuple]) -> None:
        """adds scaling for image by source.
        This is called when first image is created.
        (overwritten in image_background_manager)
        """
        if type(source) == str:
            self.appearance.is_upscaled = True
        if type(source) == list:
            self.appearance.is_upscaled = True
        if type(source) == pygame.Surface:
            pass
        if type(source) == tuple:
            self.appearance.is_scaled = True

    @staticmethod
    def get_surface_from_color(color: tuple) -> pygame.Surface:
        surf = pygame.Surface((1, 1), pygame.SRCALPHA)
        surf.fill(color)
        return surf

    def add_image_from_color(self, color: tuple) -> int:
        surf = ImageManager.get_surface_from_color(color)
        self.images_list.append({"image": surf, "type": ImageManager.COLOR, "source": color})
        self.appearance.set_dirty("all", self.appearance.LOAD_NEW_IMAGE)
        return len(self.images_list) - 1

    def get_source_from_current_image(self) -> Union[str, pygame.Surface, tuple]:
        """Returns color, path or surface"""
        return self.images_list[self.image_index]["source"]

    def is_image(self) -> bool:
        """Returns true, if current image is image (not color, or any surface)"""
        return self.images_list[self.image_index]["type"] == ImageManager.IMAGE

    def add_image_from_paths(self, paths: str) -> int:
        for path in paths:
            self.add_image_from_path(path)
        return len(self.images_list) - 1

    def add_image_from_path(self, path: str) -> int:
        path = self.find_image_file(path)
        # set image by path
        _image = self.load_image(path)
        self.images_list.append({"image": _image, "type": ImageManager.IMAGE, "source": path})
        self.appearance.set_dirty("all", self.appearance.LOAD_NEW_IMAGE)
        return len(self.images_list) - 1

    def add_image_from_appearance(self, appearance, index):
        appearance.image_manager.get_surface(index)

    def add_image_from_surface(self, surface) -> int:
        """Adds an image to the appearance

        Args:
            surface: A pygame Surface

        Returns:
            Index of the created image.
        """
        self.images_list.append({"image": surface, "type": ImageManager.SURFACE, "source": None})
        self.appearance.set_dirty("all", self.appearance.LOAD_NEW_IMAGE)
        return len(self.images_list) - 1

    def get_surface(self, index):
        try:
            return self.images_list[index]
        except Exception:
            raise ImageIndexNotExistsError(index, self)

    def replace_image(self, image, type, source):
        self.images_list[self.image_index] = {"image": image, "type": type, "source": source}
        self.appearance.set_dirty("all", self.appearance.LOAD_NEW_IMAGE)

    def reset_image_index(self):
        if self.current_animation_images:
            self.image_index = len(self.images_list) - 1

    def next_image(self):
        """Switches to the next image of the appearance."""
        if self.appearance.is_animated:
            if self.image_index < len(self.images_list) - 1:
                self.image_index = self.image_index + 1
            else:
                if not self.appearance.loop:
                    self.appearance.is_animated = False
                    self.appearance.after_animation()
                self.image_index = 0
            self.appearance.set_dirty("all", self.appearance.LOAD_NEW_IMAGE)

    def first_image(self):
        """Switches to the first image of the appearance."""
        self.image_index = 0
        # self.set_dirty("all", self.appearance.LOAD_NEW_IMAGE)

    def load_image_from_image_index(self):
        if self.images_list and self.image_index < len(self.images_list) and self.images_list[self.image_index]:
            # if there is an image list load image by index
            image = self.images_list[self.image_index]["image"]
        else:  # no image files - Render raw surface
            image = self.load_surface()
        return image

    def set_image_index(self, value) -> bool:
        if value == -1:
            value = len(self.images_list) - 1
        if 0 <= value < len(self.images_list):
            old_index = self.image_index
            self.image_index = value
            if old_index != self.image_index:
                self.appearance.set_dirty("all", self.appearance.LOAD_NEW_IMAGE)
            return True
        else:
            raise ImageIndexNotExistsError(value, self)

    def load_surface(self) -> pygame.Surface:
        if not self.appearance.surface_loaded:
            image = pygame.Surface((self.appearance.parent.width, self.appearance.parent.height), pygame.SRCALPHA)
            image.set_alpha(255)
            return image

    def end_animation(self, appearance):
        appearance.is_animated = False
        appearance.loop = False
        appearance.set_image(0)
        self.animation_frame = 0

    def remove_last_image(self):
        del self.images_list[-1]
        self.appearance.set_image(-1)
        self.appearance.set_dirty("all", self.appearance.LOAD_NEW_IMAGE)
