import os
from pathlib import Path

from miniworldmaker.base import app


class FileManager:

    @staticmethod
    def relative_to_absolute_path(path):
        canonical_path = str(path).replace('/', os.sep).replace('\\', os.sep)
        return canonical_path

    @staticmethod
    def has_ending(path):
        return "." in path

    @staticmethod
    def get_path_with_file_ending(path, file_endings):
        # 1. search for file
        if app.App.path:
            relative_path = app.App.path + "/" + path
        else:
            relative_path = path
        if Path(relative_path).is_file():
            full_path = FileManager.relative_to_absolute_path(relative_path)
            return full_path
        # 2. search for file with file endings
        full_path = FileManager._get_full_path_for_endings("", path, file_endings)
        if full_path:
            return full_path
        # 3. search for file with file endings in image sub folder
        full_path = FileManager._get_full_path_for_endings("images/", path, file_endings)
        if full_path:
            return full_path
        # 4 Auto correct wrong file endings
        if "." in path:
            path_without_ending = path.split(".")[0]
            full_path = FileManager._get_full_path_for_endings("", path_without_ending, file_endings)
            if full_path:
                return full_path
            full_path = FileManager._get_full_path_for_endings("images/", path_without_ending, file_endings)
            if full_path:
                return full_path
        raise FileNotFoundError(path)

    @staticmethod
    def _get_full_path_for_endings(prefix, path, file_endings):
        for filename_extension in file_endings:
            relative_path = prefix + path + "." + filename_extension
            if app.App.path:
                relative_path = app.App.path + "/" + relative_path
            if Path(relative_path).is_file():
                full_path = FileManager.relative_to_absolute_path(relative_path)
                return full_path

    @staticmethod
    def get_image_path(path):
        canonical_path = FileManager.relative_to_absolute_path(path)
        if Path(canonical_path).is_file():
            return Path(canonical_path)
        else:
            return FileManager.get_path_with_file_ending(path, ["jpg", "jpeg", "png", "JPG", "JPEG", "PNG"])
            # else:
            #    return file_manager.FileManager.get_path_with_file_ending(
            #        canonical_path.split(".")[0], ["jpg", "jpeg", "png"]
            #    )
