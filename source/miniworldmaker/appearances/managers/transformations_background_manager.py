import pygame
from miniworldmaker.appearances.managers import transformations_manager


class TransformationsBackgroundManager(transformations_manager.TransformationsManager):
    def __init__(self, appearance):
        super().__init__(appearance)
        self.transformations_pipeline = [
            ("scale_to_tile", self.transformation_scale_to_tile, "is_scaled_to_tile")
        ] + self.transformations_pipeline
        self.transformations_pipeline.append(("grid_overlay", self.transformation_show_grid, "grid_overlay"))

    def transformation_show_grid(self, image: pygame.Surface, appearance) -> pygame.Surface:
        parent = appearance.parent
        i = 0
        while i <= parent.width:
            pygame.draw.rect(image, self.color, [i, 0, parent.tile_margin, parent.height])
            i += parent.tile_size + parent.tile_margin
        i = 0
        while i <= parent.height:
            pygame.draw.rect(image, self.color, [0, i, parent.width, parent.tile_margin])
            i += parent.tile_size + parent.tile_margin
        return image

    def transformation_scale_to_tile(self, image: pygame.Surface, appearance) -> pygame.Surface:
        parent = appearance.parent
        image = pygame.transform.scale(image, (parent.tile_size, parent.tile_size))
        with_margin = pygame.Surface((parent.tile_size + parent.tile_margin, parent.tile_size + parent.tile_margin))
        with_margin.blit(image, (parent.tile_margin, parent.tile_margin))
        return with_margin
