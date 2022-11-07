import pygame


class Channel:
    def __init__(self, pygame_channel: pygame.mixer.Channel, path: str):
        self.pygame_channel: pygame.mixer.Channel = pygame_channel
        self.path : str = path
        self._is_playing = True
        self.stopped = False
        self.volume = 100
        self.set_volume(100)

    def pause(self):
        self.pygame_channel.pause()
        self._is_playing = False

    def is_playing(self) -> bool:
        return self._is_playing

    def unpause(self):
        self.pygame_channel.unpause()
        self._is_playing = True

    def stop(self):
        self.pygame_channel.stop()
        self._is_playing = False
        self.stopped = True

    def set_volume(self, volume):
        if volume > 100:
            volume = 100
        elif volume < 0:
            volume = 0
        self.volume = volume
        if self.pygame_channel:
            self.pygame_channel.set_volume(volume / 100)

    def get_volume(self):
        return self.volume
