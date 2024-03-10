from collections import defaultdict

import pygame


class TransformationsManager:
    def __init__(self, appearance):
        self.surface = None
        self.appearance = appearance
        self.reload_transformations = defaultdict()
        """Structure: {'orientation': False, 'texture': True, ...}
        False: The Transformation is loaded from cache
        True: The transformation is reloaded 
        """
        self.cached_image = pygame.Surface((0, 0))
        self.cached_images = defaultdict()
        self.transformations_pipeline = [
            (
                "orientation",
                self.transformation_set_orientation,
                "orientation",
                False,
            ),  # first, so that scale works on correct aspect-ratio
            ("texture", self.transformation_texture, "is_textured", False),
            ("scale", self.transformation_scale, "is_scaled", False),
            ("scale_to_width", self.transformation_scale_to_width, "is_scaled_to_width", False),
            ("scale_to_height", self.transformation_scale_to_height, "is_scaled_to_height", False),
            ("upscale", self.transformation_upscale, "is_upscaled", False),
            ("flip", self.transformation_flip, "is_flipped", False),
            ("coloring", self.transformation_coloring, "coloring", False),
            ("transparency", self.transformation_transparency, "transparency", False),
            ("write_text", self.transformation_write_text, "text", False),
            ("draw_images", self.transformation_draw_images, "draw_images", False),
            ("draw_shapes", self.transformation_draw_shapes, "draw_shapes", False),
            ("rotate", self.transformation_rotate, "is_rotatable", False),
        ]

    def get_size(self):
        return self.appearance.parent.size

    def get_width(self):
        return self.get_size()[0]

    def get_height(self):
        return self.get_size()[1]

    def blit(self, image: "pygame.Surface"):
        """helper function:
        creates new surface with parent_size and blits transformed image to
        this surface.
        """
        self.surface = pygame.Surface(self.get_size(), pygame.SRCALPHA)
        if self.appearance.is_centered:
            x = (self.surface.get_width() - image.get_width()) / 2
            y = (self.surface.get_height() - image.get_height()) / 2
        else:
            x, y = 0, 0
        self.surface.blit(image, (x, y))

    def reset_reload_transformations(self):
        """All, reload_transformations will be set to false
        => next image will completly loaded from cache.
        """
        for key in self.reload_transformations.keys():
            self.reload_transformations[key] = False

    def process_transformation_pipeline(self, image, appearance):
        """Processes the transformation pipeline for a given image.

        The transformations pipeline will be loaded from cache, if nothing is cleared
        """
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
                if getattr(appearance, transformation[2]) and self.get_size() != (0, 0):
                    image = self.cached_images[transformation[0]]  # Reload image from cache
            else:  # reload_transformations is true
                if getattr(appearance, transformation[2]) and self.get_size() != (0, 0):
                    # perform image action
                    if image.get_width() != 0 and image.get_height() != 0:
                        image = transformation[1](image, appearance)
                        self.cached_images[transformation[0]] = image
        return image

    def transformation_texture(self, image, appearance):
        background = pygame.Surface((appearance.parent.width, appearance.parent.height))
        if appearance.texture_size[0] != 0:
            texture_width = appearance.texture_size[0]
        else:
            if not hasattr(appearance.parent, "tile_size") or appearance.parent.tile_size == 1:
                texture_width = image.get_width()
            else:
                texture_width = appearance.parent.tile_size
        if appearance.texture_size[1] != 0:
            texture_height = appearance.texture_size[1]
        else:
            if not hasattr(appearance.parent, "tile_size") or appearance.parent.tile_size == 1:
                texture_height = image.get_width()
            else:
                texture_height = appearance.parent.tile_size
        image = pygame.transform.scale(image, (texture_width, texture_height))
        background.fill((255, 255, 255))
        i, j, width, height = 0, 0, 0, 0
        while width < appearance.parent.width:
            while height < appearance.parent.height:
                width = i * texture_width
                height = j * texture_height
                j += 1
                background.blit(image, (width, height))
            j, height = 0, 0
            i += 1
        self.blit(background)
        return self.surface

    def transformation_upscale(self, image: pygame.Surface, appearance) -> pygame.Surface:
        parent = appearance.parent
        if self.get_size() != 0:
            scale_factor_x = self.get_size()[0] / image.get_width()
            scale_factor_y = self.get_size()[1] / image.get_height()
            scale_factor = min(scale_factor_x, scale_factor_y)
            new_width = int(image.get_width() * scale_factor)
            new_height = int(image.get_height() * scale_factor)
            image = pygame.transform.scale(image, (new_width, new_height))
        self.blit(image)
        return self.surface

    def transformation_scale(
            self,
            image: pygame.Surface,
            appearance,
    ) -> pygame.Surface:
        size = self.get_size()
        image = pygame.transform.scale(image, size)
        self.blit(image)
        return self.surface

    def transformation_scale_to_height(
            self,
            image: pygame.Surface,
            appearance,
    ) -> pygame.Surface:
        parent = appearance.parent
        scale_factor = self.get_height() / image.get_height()
        new_width = int(image.get_width() * scale_factor)
        new_height = int(image.get_height() * scale_factor)
        image = pygame.transform.scale(image, (new_width, new_height))
        self.blit(image)
        return self.surface

    def transformation_scale_to_width(
            self,
            image: pygame.Surface,
            appearance,
    ) -> pygame.Surface:
        parent = appearance.parent
        scale_factor = self.get_width() / image.get_width()
        new_width = int(image.get_width() * scale_factor)
        new_height = int(image.get_height() * scale_factor)
        image = pygame.transform.scale(image, (new_width, new_height))
        self.blit(image)
        return self.surface

    def transformation_rotate(self, image: pygame.Surface, appearance) -> pygame.Surface:
        if appearance.parent.direction != 0:
            rotated_image = pygame.transform.rotozoom(image, -(appearance.parent.direction), 1)
            self.surface = rotated_image
            return rotated_image
        else:
            self.surface = image
            return image

    def transformation_set_orientation(self, image: pygame.Surface, appearance) -> pygame.Surface:
        if appearance.parent.orientation != 0:
            image = pygame.transform.rotate(image, -appearance.parent.orientation)
            return image
        else:
            return image

    def transformation_flip(self, image: pygame.Surface, appearance) -> pygame.Surface:
        flipped_image = pygame.transform.flip(image, appearance.is_flipped, False)
        self.blit(flipped_image)
        return self.surface

    def transformation_coloring(self, image: pygame.Surface, appearance) -> pygame.Surface:
        parent = appearance.parent
        image = image.copy()
        # zero out RGB values
        # image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)  # Fill black
        # add in new RGB values
        parent_color = self.appearance.parent.fill_color
        color_withour_alpha = parent_color[0:3] + (0,)
        image.fill(parent_color, None)  # Add color
        # append alpha
        new_color = parent_color
        # image.fill(new_color, None, pygame.BLEND_RGBA_MULT)  # Multiply transparency
        self.surface = image
        return self.surface

    def transformation_transparency(self, image: pygame.Surface, appearance) -> pygame.Surface:
        """ """
        image.set_alpha(appearance.alpha)
        self.surface = image
        return image

    @staticmethod
    def crop_image(self, image: pygame.Surface, parent, appearance) -> pygame.Surface:
        cropped_surface = pygame.Surface(self.get_size())
        cropped_surface.fill((255, 255, 255))
        cropped_surface.blit(image, (0, 0), (0, 0, self.get_size()))
        self.blit(cropped_surface)
        return self.surface

    def transformation_write_text(self, image: pygame.Surface, appearance) -> pygame.Surface:
        text_surf = appearance.font_manager.transformation_write_text(image, appearance, appearance.color)
        self.surface = text_surf
        return text_surf

    def transformation_draw_images(self, image: pygame.Surface, appearance) -> pygame.Surface:
        for draw_action in appearance.draw_images:
            surface = draw_action[0]
            rect = draw_action[1]
            surface = pygame.transform.scale(surface, (rect[2], rect[3]))
            image.blit(surface, rect)
        self.surface = image
        return image

    def transformation_draw_shapes(self, image: pygame.Surface, appearance) -> pygame.Surface:
        for draw_action in appearance.draw_shapes:
            draw_action[0](image, *draw_action[1])
        self.surface = image
        return image

    def flag_reload_actions_for_transformation_pipeline(self, transformation_string):
        """Reloads transformations in transformation pipeline with given transformation string.
        
        e.g. "scale": reloads everything after scale. Actions before scale are loaded from cache.

        Pipeline:
        texture, scale, upscale, flip, coloring, transparency, write_text, draw_images, draw_shapes, rotate
        """
        reload = False
        for transformation in self.transformations_pipeline:
            if transformation[0] == transformation_string or transformation_string == "all":
                reload = True  # reload image action
            if reload:
                self.reload_transformations[transformation[0]] = True  # reload all actions starting with image action
        if self.appearance.parent:
            self.appearance.parent.dirty = 1
