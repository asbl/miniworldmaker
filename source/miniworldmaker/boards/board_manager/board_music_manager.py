from miniworldmaker.base import app as app_mod
from typing import Optional


class BoardMusicManager:
    def __init__(self, app: "app_mod.App"):
        self.app: "app_mod.App" = app
        self.sound_manager = self.app.sound_manager

    def pause(self):
        """pauses a music
        """
        self.sound_manager.pause_music()

    def is_playing(self) -> bool:
        """returns True, if board is playing a music (and music ist not paused")
        """
        return self.sound_manager.is_music_playing()

    def get_path(self) -> str:
        """gets path to current music

        Returns:
            The path to current music file
        """
        return self.sound_manager.get_music_path()

    def play(self, path: Optional[str] = None):
        """plays a music from path

        Args:
            path: The path to the music

        Returns:

        """
        self.sound_manager.play_music(path)

    def stop(self):
        """stops a music

        Returns:

        """
        self.sound_manager.stop_music()

    def set_volume(self, volume: float):
        """sets volume of music

        Args:
            volume: Volume between 0 and 100
        """
        self.sound_manager.set_music_volume(volume)

    def get_volume(self) -> float:
        """gets volume of music

        Returns:
            current volume

        """
        return self.sound_manager.get_music_volume()
