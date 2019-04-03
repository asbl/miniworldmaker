import pygame


class Area(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.surface = pygame.Surface((rect.width, rect.height))
        self.rect = pygame.Rect(rect)
