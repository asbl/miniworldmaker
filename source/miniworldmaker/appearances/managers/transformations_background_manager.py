import pygame
from miniworldmaker.appearances.managers import transformations_manager


class TransformationsBackgroundManager(transformations_manager.TransformationsManager):
    def __init__(self, appearance):
        super().__init__(appearance)
        self.transformations_pipeline.append(("grid", self.transformation_grid, "grid"))

    def transformation_grid(self, image: pygame.Surface, appearance) -> pygame.Surface:
        parent = appearance.parent
        print("show grid", appearance.color, parent.width, parent.height)
        i = 0
        j = 0
        print(image)
        while i <= parent.width:
            pygame.draw.line(image, appearance.color,(0,i),(parent.width, i), 1)
            i += parent.tile_size
        while j <= parent.height:
                pygame.draw.line(image, appearance.color,(j,0),(j, parent.height), 1)
                j += parent.tile_size 
            
        return image
