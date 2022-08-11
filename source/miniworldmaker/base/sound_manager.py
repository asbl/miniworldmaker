import pygame

import miniworldmaker.base.app as app_mod
from typing import Dict


class SoundManager:
    def __init__(self, app: "app_mod.App"):
        self.sound_effects: Dict[str, pygame.mixer.Sound] = {}
        self.app: "app_mod.App" = app
        self.volume = 100
        pygame.mixer.init()

    def register_sound(self, path) -> pygame.mixer.Sound:
        """
        Registers a sound effect to board-sound effects library

        Args:
            path: The path to sound

        Returns:
            the sound

        """
        try:
            effect: pygame.mixer.Sound = pygame.mixer.Sound(path)
            self.sound_effects[path] = effect
            return effect
        except pygame.error:
            raise FileExistsError("File '{0}' does not exist. Check your path to the sound.".format(path))

    def play_sound(self, path: str):
        if path.endswith("mp3"):
            path = path[:-4] + "wav"
        if path in self.sound_effects.keys():
            self.sound_effects[path].play()
        else:
            effect = self.register_sound(path)
            effect.play()

    def set_volume(self, volume, path: str = None):
        """Sets volume (max: 100, min: 0)
        """
        if path:
            self.sound_effects[path].set_volume(volume / 100)
        else:
            for key, sound_effect in self.sound_effects.items():
                sound_effect.set_volume(volume / 100)

    def stop(self, volume, path: str = None):
        """Sets volume (max: 100, min: 0)
        """
        if path:
            self.sound_effects[path].stop()
        else:
            for key, sound_effect in self.sound_effects.items():
                sound_effect.stop()