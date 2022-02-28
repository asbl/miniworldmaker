import pygame
from collections import defaultdict


class TransformationsManager:
    def __init__(self, appearance):
        self.reload_transformations = defaultdict()
        self.cached_image = pygame.Surface((0, 0))
        self.cached_images = defaultdict()
        self.transformations_pipeline = [
            ("orientation", self.transformation_set_orientation, "orientation", False),
            ("texture", self.transformation_texture, "is_textured", False),
            ("scale", self.transformation_scale, "is_scaled", False),
            ("scale_to_width", self.transformation_scale_to_width, "is_scaled_to_width", False),
            ("scale_to_height", self.transformation_scale_to_height, "is_scaled_to_height", False),
            ("upscale", self.transformation_upscale, "is_upscaled", False),
            ("flip", self.transformation_flip, "is_flipped", False),
            ("coloring", self.transformation_coloring, "coloring", False),
            ("transparency", self.transformation_transparency, "transparency", False),
            ("write_text", self.transformation_write_text, "text", False),
            ("draw_shapes", self.transformation_draw_shapes, "draw_shapes", False),
            ("rotate", self.transformation_rotate, "is_rotatable", False),
            ("flip_vertical", self.transformation_flip_vertical, "flip_vertical", False),
        ]

    def reset_reload_transformations(self):
        for key in self.reload_transformations.keys():
            self.reload_transformations[key] = False

    def process_transformation_pipeline(self, image, appearance):
        for transformation in self.transformations_pipeline:
            # If an image action is to be executed again,
            # load the last cached image from the pipeline and execute
            # all subsequent image actions.
            if (
                transformation[0] in self.reload_transformations
                and self.reload_transformations[transformation[0]] is False
                and transformation[0] in self.cached_images.keys()
                and self.cached_images[transformation[0]]
            ):
                if getattr(appearance, transformation[2]) and appearance.parent.size != (0, 0):
                    image = self.cached_images[transformation[0]]  # Reload image from cache
            else:  # reload_transformations is true
                if getattr(appearance, transformation[2]) and appearance.parent.size != (0, 0):
                    # perform image action
                    if image.get_width() != 0 and image.get_height!=0:
                        image = transformation[1](image, appearance)
                        self.cached_images[transformation[0]] = image
        #appearance.parent.dirty = 1
        return image

    def transformation_texture(self, image, appearance):
        background = pygame.Surface((appearance.parent.width, appearance.parent.height))
        background.fill((255, 255, 255))
        i, j, width, height = 0, 0, 0, 0
        while width < appearance.parent.width:
            while height < appearance.parent.height:
                width = i * image.get_width()
                height = j * image.get_height()
                j += 1
                background.blit(image, (width, height))
            j, height = 0, 0
            i += 1
        return background

    def transformation_upscale(self, image: pygame.Surface, appearance) -> pygame.Surface:
        parent = appearance.parent
        if parent.size != 0:
            scale_factor_x = parent.width / image.get_width()
            scale_factor_y = parent.height / image.get_height()
            scale_factor = min(scale_factor_x, scale_factor_y)
            new_width = int(image.get_width() * scale_factor)
            new_height = int(image.get_height() * scale_factor)
            image = pygame.transform.scale(image, (new_width, new_height))
        return image

    def transformation_scale(
        self,
        image: pygame.Surface,
        appearance,
    ) -> pygame.Surface:
        image = pygame.transform.scale(image, (appearance.parent.width, appearance.parent.height))
        return image

    def transformation_scale_to_height(
        self,
        image: pygame.Surface,
        appearance,
    ) -> pygame.Surface:
        parent = appearance.parent
        scale_factor = parent.height / image.get_height()
        new_width = int(image.get_width() * scale_factor)
        new_height = int(image.get_height() * scale_factor)
        image = pygame.transform.scale(image, (new_width, new_height))
        return image

    def transformation_scale_to_width(
        self,
        image: pygame.Surface,
        appearance,
    ) -> pygame.Surface:
        parent = appearance.parent
        scale_factor = parent.width / image.get_width()
        new_width = int(image.get_width() * scale_factor)
        new_height = int(image.get_height() * scale_factor)
        image = pygame.transform.scale(image, (new_width, new_height))
        return image

    def transformation_rotate(self, image: pygame.Surface, appearance) -> pygame.Surface:
        if appearance.parent.direction != 0:
            rotated_image = pygame.transform.rotozoom(image, -(appearance.parent.direction), 1)
            return rotated_image
        else:
            return image

    def transformation_flip_vertical(self, image: pygame.Surface, appearance) -> pygame.Surface:
        if appearance.parent.direction < 0:
            return pygame.transform.flip(image, True, False)
        else:
            return image

    def transformation_set_orientation(self, image: pygame.Surface, appearance) -> pygame.Surface:
        if appearance.parent.orientation != 0:
            return pygame.transform.rotate(image, -appearance.parent.orientation)
        else:
            return image

    def transformation_flip(self, image: pygame.Surface, appearance) -> pygame.Surface:
        return pygame.transform.flip(image, appearance.is_flipped, False)

    def transformation_coloring(self, image: pygame.Surface, appearance) -> pygame.Surface:
        """
        Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
        original).

        :param image: Surface to create a colorized copy of
        :param newColor: RGB color to use (original alpha values are preserved)
        :return: New colorized Surface instance
        """
        parent = appearance.parent
        image = image.copy()
        # zero out RGB values
        image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)  # Fill black
        # add in new RGB values
        new_color = self.color[0:3] + (0,)
        image.fill(new_color, None, pygame.BLEND_RGBA_ADD)  # Add color
        new_color = (255, 255, 255) + (self.color[3],)
        image.fill(new_color, None, pygame.BLEND_RGBA_MULT)  # Multiply transparency
        return image

    def transformation_transparency(self, image: pygame.Surface, appearance) -> pygame.Surface:
        """ """
        image.set_alpha(appearance.alpha)
        return image

    @staticmethod
    def crop_image(self, image: pygame.Surface, parent, appearance) -> pygame.Surface:
        cropped_surface = pygame.Surface((appearance.parent.width, appearance.parent.height))
        cropped_surface.fill((255, 255, 255))
        cropped_surface.blit(image, (0, 0), (0, 0, (appearance.parent.width, appearance.parent.height)))
        return cropped_surface

    def transformation_write_text(self, image: pygame.Surface, appearance) -> pygame.Surface:
        return appearance.font_manager.transformation_write_text(image, appearance, appearance.color)

    def transformation_draw_shapes(self, image: pygame.Surface, appearance) -> pygame.Surface:
        for draw_action in appearance.draw_shapes:
            draw_action[0](image, *draw_action[1])
        return image

    def reload_transformations_after(self, transformation_string):
        reload = False
        for transformation in self.transformations_pipeline:
            if transformation[0] == transformation_string or transformation_string == "all":
                reload = True  # reload image action
            if reload:
                self.reload_transformations[transformation[0]] = True  # reload all actions after image action
