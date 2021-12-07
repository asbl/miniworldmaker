import os
from pathlib import Path


class FileManager:

    @staticmethod
    def relative_to_absolute_path(path):
        canonicalized_path = str(path).replace('/', os.sep).replace('\\', os.sep)
        return canonicalized_path

    @staticmethod
    def has_ending(path):
        return "." in path

    @staticmethod
    def get_path_with_file_ending(path, ending):
        for filename_extension in ending:
            if Path(path + "." + filename_extension).is_file():
                print(path + "." + filename_extension)
                full_path = FileManager.relative_to_absolute_path(path + "." + filename_extension)
                return full_path
        # No file ending found:
        raise FileNotFoundError(path)
