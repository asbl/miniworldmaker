import pygame

import miniworldmaker.base.app as app_mod


class MusicManager:
    def __init__(self, app: "app_mod.App"):
        self.app: "app_mod.App" = app
        self.path = None
        pygame.mixer.init()

    def change_music(self, path):
        self.stop_music()
        self.path = path
        pygame.mixer.music.load(self.path)

    def load_music(self, path):
        self.path = path
        pygame.mixer.music.load(self.path)

    def play_music(self, path, loop):
        """plays a music by path
        """
        if path:
            self.load_music(path)
        self.load_music(self.path)
        pygame.mixer.music.play(loop)

    def is_playing(self):
        return pygame.mixer.music.get_busy()

    def stop_music(self):
        """stops current music
        """
        pygame.mixer.music.stop()

    def fade_out(self, time):
        """fades current music out
        """
        pygame.mixer.music.fadeout(time)

    def fade_in(self, time):
        """Alternative to play

        Returns:

        """
        pygame.mixer.music.play(- 1, 0, time)

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    @property
    def volume(self):
        return self.get_volume()

    @volume.setter
    def volume(self, value):
        return self.set_volume(value)

    def set_volume(self, percent):
        """Sets volume
        min: 0
        max: 100
        """
        pygame.mixer.music.set_volume(percent / 100)

    def get_volume(self):
        """Gets actual volume
        min: 0
        max: 100
        """
        return pygame.mixer.music.get_volume() * 100

