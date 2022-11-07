import pygame

import miniworldmaker.base.app as app_mod


class MusicManager:
    def __init__(self, app: "app_mod.App"):
        self.app: "app_mod.App" = app
        pygame.mixer.init()

    def change_music(self, path):
        self.stop_music()
        pygame.mixer.music.load(path)

    def load_music(self, path):
        pygame.mixer.music.load(path)

    def play_music(self, path: str):
        """plays a music by path

        Args:
            path: The path to the music

        Returns:

        """
        self.load_music(path)
        music = pygame.mixer.Sound(path)
        pygame.mixer.music.play(-1)

    def is_playing(self):
        return True



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
        pygame.mixer.pause()

    def unpause(self):
        pygame.mixer.unpause()

    def set_volume(self, percent):
        """Sets volume
        min: 0
        max: 100
        """
        pygame.mixer.Sound.set_volume(percent / 100)

    def get_volume(self, percent):
        """Gets volume
        min: 0
        max: 100
        """
        pygame.mixer.Sound.set_volume(percent * 100)

