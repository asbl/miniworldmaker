import pygame
import os
from pathlib import Path
from miniworldmaker.app import file_manager
from miniworldmaker.exceptions.miniworldmaker_exception import ImageIndexNotExistsError


class ImageManager:
    """Handles loading and caching of images."""

    _images_dict = {}  # dict with key: image_path, value: loaded image

    def __init__(self):
        self.animation_frame = 0
        self.current_animation_images = None
        self.image_index = 0  # current_image index (for animations)
        self.images_list = []  # Original images
        self.image_paths = []  # list with all images

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

    def setup_images(self):
        from pathlib import Path
        from miniworldmaker.appearances import appearance

        jpgs = list(Path("./images/").rglob("*.[jJ][pP][gG]"))
        jpegs = list(Path("./images/w wwsdsdwasd").rglob("*.[jJ][pP][eE][gG]"))
        pngs = list(Path("./images/").rglob("*.[pP][nN][gG]"))
        images = jpgs + jpegs + pngs
        for img_path in images:
            self.load_image(img_path)

    def add_image(self, path: str, appearance) -> int:
        """Adds an image to the appearance

        Args:
            path (str): Path to the image relative to actual directory

        Returns:
            Index of the created image.
        """
        path = self.find_image_file(path)
        # set image by path
        _image = self.load_image(path)
        appearance.image_manager.images_list.append(_image)
        appearance.image_manager.image_paths.append(path)
        appearance.dirty = 1
        appearance._reload_all()
        return len(appearance.image_manager.images_list) - 1

    def add_image_from_surface(self, surface, appearance) -> int:
        """Adds an image to the appearance

        Args:
            path (str): Path to the image relative to actual directory

        Returns:
            Index of the created image.
        """
        appearance.image_manager.images_list.append(surface)
        appearance.dirty = 1
        appearance._reload_all()
        return len(appearance.image_manager.images_list) - 1

    def replace_image(self, surface, index, appearance):
        appearance.image_manager.images_list[index] = surface
        appearance.dirty = 1
        appearance._reload_all()

    def reset(self):
        self.set_image_index(0)
        self.end_animation(self)

    def reset_image_index(self):
        if self.current_animation_images:
            _rect = self.token.costume.image.get_rect()
            self.image_index = len(self.images_list) - 1

    async def update(self, appearance):
        if appearance.is_animated:
            self.animation_frame += 1
            if self.animation_frame == appearance.animation_speed:
                await self.next_image(appearance)
                self.animation_frame = 0
        appearance._reload_image()

    async def next_image(self, appearance):
        """Switches to the next image of the appearance."""
        if appearance.is_animated:
            if self.image_index < len(self.images_list) - 1:
                self.image_index = self.image_index + 1
            else:
                if not appearance.loop:
                    appearance.is_animated = False
                    appearance.after_animation()
                self.image_index = 0
            appearance.parent.dirty = 1
            appearance.reload_transformations_after("all")

    async def first_image(self):
        """Switches to the first image of the appearance."""
        self.image_index = 0
        self.dirty = 1
        self.parent.dirty = 1
        self.reload_transformations_after("all")

    def load_image_by_image_index(self, appearance):
        if self.images_list and self.image_index < len(self.images_list) and self.images_list[self.image_index]:
            # if there is a image list load image by index
            image = self.images_list[self.image_index]
        else:  # no image files - Render raw surface
            image = self.load_surface(appearance)
        return image

    def set_image_index(self, value, appearance) -> bool:
        if value == -1:
            value = len(self.images_list) - 1
        if 0 <= value < len(self.images_list):
            self.image_index = value
            appearance.dirty = 1
            appearance.parent.dirty = 1
            appearance.reload_transformations_after("all")
            return True
        else:
            raise ImageIndexNotExistsError()

    def load_surface(self, appearance) -> pygame.Surface:
        if not appearance.surface_loaded:
            image = pygame.Surface((appearance.parent.width, appearance.parent.height), pygame.SRCALPHA)
            image.fill(appearance.fill_color)
            image.set_alpha(255)
            appearance.raw_image = image
            return image

    def end_animation(self, appearance):
        appearance.is_animated = False
        appearance.loop = False
        appearance.set_image(0)
        self.animation_frame = 0

    def remove_last_image(self, appearance):
        del self.images_list[-1]
        self.set_image(-1)
        appearance.reload_transformations_after("all")

    def remove_image(self, appearance):
        pass
