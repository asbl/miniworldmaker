import pygame
import math
from miniworldmaker.appearances.managers import transformations_manager


class TransformationsCostumeManager(transformations_manager.TransformationsManager):
    def __init__(self, appearance):
        super().__init__(appearance)
        self.transformations_pipeline.append(("info_overlay", self.transformation_info_overlay, "info_overlay"))

    def transformation_info_overlay(self, image: pygame.Surface, appearance) -> pygame.Surface:
        parent = appearance.parent
        pygame.draw.rect(image, (255, 0, 0, 100), image.get_rect(), 4)
        # draw direction marker on image
        rect = parent.rect
        center = rect.centerx - parent.x, rect.centery - parent.y
        x = center[0] + math.sin(math.radians(parent.direction)) * rect.width / 2
        y = center[1] - math.cos(math.radians(parent.direction)) * rect.width / 2
        start_pos, end_pos = (center[0], center[1]), (x, y)
        pygame.draw.line(image, (255, 0, 0, 100), start_pos, end_pos, 3)
        return image
