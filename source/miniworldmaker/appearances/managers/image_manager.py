import pygame
import os
from pathlib import Path
from miniworldmaker.base import file_manager
from miniworldmaker.exceptions.miniworldmaker_exception import ImageIndexNotExistsError
from typing import List, Union, Tuple
from pathlib import Path

class ImageManager:
    """Handles loading and caching of images."""

    _images_dict = {}  # dict with key: image_path, value: loaded image

    def __init__(self, appearance):
        self.animation_frame = 0
        self.current_animation_images = None
        self.image_index = 0  # current_image index (for animations) in self.image_lists
        self.images_list: List["pygame.Surface"] = []  # Original images - remove or add image surfaces here
        self.image_paths: List[str] = []  # list with all images paths
        self.appearance = appearance
        self.has_image = False
        self.add_default_image()

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
            canonicalized_path = str(path).replace("/", os.sep).replace("\\", os.sep)
            if canonicalized_path in ImageManager._images_dict.keys():
                # load image from img_dict
                _image = ImageManager._images_dict[canonicalized_path]
            else:
                try:
                    _image = pygame.image.load(canonicalized_path).convert_alpha()
                    ImageManager._images_dict[canonicalized_path] = _image
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
        canonicalized_path = file_manager.FileManager.relative_to_absolute_path(path)
        if Path(canonicalized_path).is_file():
            return Path(canonicalized_path)
        else:
            if not file_manager.FileManager.has_ending:
                return file_manager.FileManager.get_path_with_file_ending(path, ["jpg", "jpeg", "png"])
            else:
                return file_manager.FileManager.get_path_with_file_ending(
                    canonicalized_path.split(".")[0], ["jpg", "jpeg", "png"]
                )

    @staticmethod
    def cache_images_in_image_folder():
        """is called on program start.
        Loads all images in folder path/images
        """
        jpgs = list(Path("./images/").rglob("*.[jJ][pP][gG]"))
        jpegs = list(Path("./images/w wwsdsdwasd").rglob("*.[jJ][pP][eE][gG]"))
        pngs = list(Path("./images/").rglob("*.[pP][nN][gG]"))
        images = jpgs + jpegs + pngs
        for img_path in images:
            ImageManager.load_image(img_path)

    def add_first_image(self, source):
        if len(self.images_list) == 1:
            image = self.images_list.pop(0)
            del image
        self.add_image(source, first=True)

    def add_default_image(self):
        if not self.has_image and len(self.images_list) == 0:
            self.appearance.is_scaled = True
            surf = pygame.Surface((1, 1), pygame.SRCALPHA)
            surf.fill(self.appearance.fill_color)
            self.images_list.append(surf)
            self.appearance.dirty = 1
            return len(self.images_list) - 1

    def add_image(self, source: Union[str, pygame.Surface, Tuple], first=False) -> int:
        """Adds an image to the appearance

        Args:
            path (str): Path to the image relative to actual directory

        Returns:
            Index of the created image.
        """
        if first:
            self._add_scaling(source)
        if type(source) == str:
            return self.add_image_from_path(source)
        elif type(source) == list:
            return self.add_image_from_paths(source)
        elif type(source) == pygame.Surface:
            return self.add_image_from_surface(source)
        elif type(source) == tuple:
            return self.add_image_from_color(source)

    def _add_scaling(self, source):
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
    def get_surface_from_color(color):
        surf = pygame.Surface((1, 1), pygame.SRCALPHA)
        surf.fill(color)
        return surf

    def add_image_from_color(self, color):
        surf = ImageManager.get_surface_from_color(color)
        return self.add_image_from_surface(surf)

    def add_image_from_paths(self, paths: str) -> int:
        for path in paths:
            self.add_image_from_path(path)

    def add_image_from_path(self, path: str) -> int:
        path = self.find_image_file(path)
        # set image by path
        _image = self.load_image(path)
        self.images_list.append(_image)
        self.image_paths.append(path)
        self.appearance.reload_transformations_after(
            "all",
        )
        return len(self.images_list) - 1

    def add_image_from_appearance(self, appearance, index):
        appearance.image_manager.get_surface(index)

    def add_image_from_surface(self, surface) -> int:
        """Adds an image to the appearance

        Args:
            path (str): Path to the image relative to actual directory

        Returns:
            Index of the created image.
        """
        self.images_list.append(surface)
        self.appearance.reload_transformations_after(
            "all",
        )
        return len(self.images_list) - 1

    def get_surface(self, index):
        try:
            return self.images_list[index]
        except Exception:
            raise ImageIndexNotExistsError(index, self)

    def replace_image(self, appearance):
        self.images_list[self.image_index] = appearance
        self.appearance.reload_transformations_after(
            "all",
        )

    def reset_image_index(self):
        if self.current_animation_images:
            _rect = self.token.costume.image.get_rect()
            self.image_index = len(self.images_list) - 1

    async def update(self):
        """Loads the image,
        * switches image if neccessary
        * processes transformations pipeline if neccessary
        """
        if self.appearance.is_animated:
            self.animation_frame += 1
            if self.animation_frame == self.appearance.animation_speed:
                await self.next_image()
                self.animation_frame = 0
        self.appearance._reload_image()

    async def next_image(self):
        """Switches to the next image of the appearance."""
        if self.appearance.is_animated:
            if self.image_index < len(self.images_list) - 1:
                self.image_index = self.image_index + 1
            else:
                if not self.appearance.loop:
                    self.appearance.is_animated = False
                    self.appearance.after_animation()
                self.image_index = 0
            self.appearance.parent.dirty = 1
            self.appearance.reload_transformations_after("all")

    async def first_image(self):
        """Switches to the first image of the appearance."""
        self.image_index = 0
        self.reload_transformations_after("all")

    def load_image_by_image_index(self):
        if self.images_list and self.image_index < len(self.images_list) and self.images_list[self.image_index]:
            # if there is a image list load image by index
            image = self.images_list[self.image_index]
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
                self.appearance.reload_transformations_after("all")
            return True
        else:
            raise ImageIndexNotExistsError(value, self)

    def load_surface(self) -> pygame.Surface:
        if not self.appearance.surface_loaded:
            image = pygame.Surface((self.appearance.parent.width, self.appearance.parent.height), pygame.SRCALPHA)
            #image.fill(self.appearance.fill_color)
            image.set_alpha(255)
            return image

    def end_animation(self, appearance):
        appearance.is_animated = False
        appearance.loop = False
        appearance.set_image(0)
        self.animation_frame = 0

    def remove_last_image(self):
        del self.images_list[-1]
        self.set_image(-1)
        self.appearance.reload_transformations_after("all")


    def remove_image(self, appearance):
        pass

