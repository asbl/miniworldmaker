import pygame
from miniworldmaker.app import app


class SoundManager:

    def __init__(self, app : "miniworldmaker.App" ):
        self.sound_effects: dict = {}
        self.app: "miniworldmaker.App"  = app

    def register_sound(self, path) -> pygame.mixer.Sound:
        """
        Registers a sound effect to board-sound effects library

        Args:
            path: The path to sound

        Returns: 
            the sound

        """
        try:
            effect = pygame.mixer.Sound(path)
            self.sound_effects[path] = effect
            return effect
        except pygame.error:
            raise FileExistsError(
                "File '{0}' does not exist. Check your path to the sound.".format(path))

    def play_sound(self, path: str):
        if path.endswith("mp3"):
            path = path[:-4] + "wav"
        if path in self.sound_effects.keys():
            self.sound_effects[path].play()
        else:
            effect = self.register_sound(path)
            effect.play()

    def play_music(self, path: str):
        """
        plays a music by path

        Args:
            path: The path to the music

        Returns:

        """
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
