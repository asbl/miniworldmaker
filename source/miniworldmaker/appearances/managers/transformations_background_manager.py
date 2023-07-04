import pygame
import miniworldmaker.appearances.managers.transformations_manager as transformations_manager


class TransformationsBackgroundManager(transformations_manager.TransformationsManager):
    def __init__(self, appearance):
        super().__init__(appearance)
        self.transformations_pipeline.append(("grid", self.transformation_grid, "grid"))

    def get_size(self):
        size = (self.appearance.parent.container_width, self.appearance.parent.container_height)
        return size

    def transformation_grid(self, image: pygame.Surface, appearance) -> pygame.Surface:
        parent = self.appearance.parent
        i = 0
        j = 0
        while i <= parent.height:
            pygame.draw.line(image, appearance._grid_color, (0, i), (self.get_width(), i), 1)
            i += parent.tile_size
        while j <= parent.width:
            pygame.draw.line(image, appearance._grid_color, (j, 0), (j, self.get_height()), 1)
            j += parent.tile_size

        return image
