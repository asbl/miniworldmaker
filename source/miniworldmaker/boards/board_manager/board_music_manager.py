from miniworldmaker.base import app as app_mod
from typing import Optional

class BoardMusicManager:
    def __init__(self, app: "app_mod.App"):
        self.app: "app_mod.App" = app
        self.music_manager = self.app.music_manager


    def pause(self):
        """pauses a music
        """
        self.music_manager.pause()

    def is_playing(self) -> bool:
        """returns True, if board is playing a music (and music ist not paused)
        """
        return self.music_manager.is_playing()

    def get_path(self) -> str:
        """gets path to current music

        Returns:
            The path to current music file
        """
        return self.music_manager.path()

    def play(self, path: Optional[str] = None, loop = -1):
        """plays a music from path

        Args:
            path: The path to the music
            loop: Specifies how often the music must be repeated (-1: infinitely often)

        Returns:

        """
        self.music_manager.play_music(path, loop)

    def stop(self):
        """stops a music

        Returns:

        """
        self.music_manager.stop_music()

    def set_volume(self, volume: float):
        """sets volume of music

        Args:
            volume: Volume between 0 and 100
        """
        self.music_manager.set_volume(volume)

    def get_volume(self) -> float:
        """gets volume of music

        Returns:
            current volume

        """
        return self.music_manager.get_volume()
