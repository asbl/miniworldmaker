import pygame

import miniworldmaker.base.app as app_mod
from typing import Dict, Optional
from miniworldmaker.base import channel as channel_mod


class SoundManager:
    def __init__(self, app: "app_mod.App"):
        self.sound_effects: Dict[str, pygame.mixer.Sound] = {}
        self.app: "app_mod.App" = app
        self.volume = 100
        self._has_music = False

        pygame.mixer.init()
        pygame.mixer.set_reserved(2)
        pygame.mixer.set_num_channels(64)

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

    def play_sound(self, path: str, prio=False, volume: float = 100):
        if prio:
            self._play_high_priority(path, volume)
        else:
            self._play_low_priority(path, volume)

    def _play_low_priority(self, path: str, volume: float):
        if path in self.sound_effects.keys():
            sound = self.sound_effects[path]
            sound.set_volume(volume)
            pygame_channel = sound.play()
            channel = channel_mod.Channel(pygame_channel, path)
            channel.set_volume(volume)
            return channel
        else:
            sound = self.register_sound(path)
            sound.set_volume(volume)
            pygame_channel = sound.play()
            channel = channel_mod.Channel(pygame_channel, path)
            return channel

    def _play_high_priority(self, path: str, volume: float):
        if path in self.sound_effects.keys():
            pygame_channel = pygame.mixer.find_channel()
            sound = self.sound_effects[path]
            sound.set_volume(volume)
            pygame_channel.play(sound)
            channel = channel_mod.Channel(pygame_channel, path)
            return channel
        else:
            sound = self.register_sound(path)
            sound.set_volume(volume)
            pygame_channel = pygame.mixer.find_channel()
            pygame_channel.play(sound)
            channel = channel_mod.Channel(pygame_channel, path)
            return channel

    def set_volume(self, volume, path: str = None):
        """Sets volume (max: 100, min: 0)
        """
        if path:
            self.sound_effects[path].set_volume(volume / 100)
        else:
            for key, sound_effect in self.sound_effects.items():
                sound_effect.set_volume(volume / 100)

    def stop(self, path: str = None):
        """Sets volume (max: 100, min: 0)
        """
        if path:
            self.sound_effects[path].stop()
        else:
            for key, sound_effect in self.sound_effects.items():
                sound_effect.stop()
