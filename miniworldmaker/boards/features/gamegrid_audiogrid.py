from gamegridp import gamegrid
import pygame

class AudioGrid(gamegrid.GameGrid):
    def play_sound(self, sound_path):
        """
        Spielt einen Sound

        :param sound_path: Der Pfad zum Sound relativ zum aktuellen Verzeichnis.
        """
        effect = pygame.mixer.Sound(sound_path)
        effect.play()

    def play_music(self, music_path):
        """
        Spielt eine Musik in Endlosschleife

        :param music_path: Der Pfad zur Musikdatei relativ zum aktuellen Verzeichnis.
        """
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)