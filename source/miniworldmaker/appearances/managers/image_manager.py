import pygame
import os
from pathlib import Path
from miniworldmaker.app import file_manager

class ImageManager:
    """Handles loading and caching of images.
    """

    _images_dict = {}  # dict with key: image_path, value: loaded image

    def __init__(self):
        pass

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
        appearance.animation_manager.images_list.append(_image)
        appearance.animation_manager.image_paths.append(path)
        appearance.dirty = 1
        appearance._reload_all()
        return len(appearance.animation_manager.images_list) - 1