import pygame

class AnimationManager:
    """Handles loading and caching of images.
    """

    def __init__(self):
        self.animation_frame = 0
        self.current_animation_images = None
        self.image_index = 0  # current_image index (for animations)
        self.images_list = []  # Original images
        self.image_paths = []  # list with all images

    def reset_image_index(self):
        if self.current_animation_images:
            _rect = self.token.costume.image.get_rect()
            self.image_index = len(self.images_list) - 1

    async def update(self, appearance):
        if appearance.is_animated:
            self.animation_frame += 1
            if self.animation_frame == appearance.animation_speed:
                await self.next_image(appearance)
                self.animation_frame = 0
        appearance._reload_image()
        

    async def next_image(self, appearance):
        """Switches to the next image of the appearance."""
        if appearance.is_animated:
            if self.image_index < len(self.images_list) - 1:
                self.image_index = self.image_index + 1
            else:
                if not appearance.loop:
                    appearance.is_animated = False
                    appearance.after_animation()
                self.image_index = 0
            appearance.parent.dirty = 1
            appearance.reload_transformations_after("all")

    async def first_image(self):
        """Switches to the first image of the appearance."""
        self.image_index = 0
        self.dirty = 1
        self.parent.dirty = 1
        self.reload_transformations_after("all")

    def load_image_by_image_index(self, appearance):
        if self.images_list and self.image_index < len(self.images_list) and self.images_list[self.image_index]:
            # if there is a image list load image by index
            image = self.images_list[self.image_index]
        else:  # no image files - Render raw surface
            image = self.load_surface(appearance)
        return image

    def set_image_index(self, value, appearance)  -> bool:
        if value == -1:
            value = len(self.images_list) - 1
        if 0 <= value < len(self.images_list):
            self.image_index = value
            appearance.dirty = 1
            appearance.parent.dirty = 1
            appearance.reload_transformations_after("all")
            return True
        else:
            return False

    def load_surface(self, appearance) -> pygame.Surface:
        if not appearance.surface_loaded:
            image = pygame.Surface((appearance.parent.width, appearance.parent.height), pygame.SRCALPHA)
            image.fill(appearance.fill_color)
            image.set_alpha(255)
            appearance.raw_image = image
            return image

    def end_animation(self, appearance):
        appearance.is_animated = False
        appearance.loop = False
        appearance.set_image(0)
        self.animation_frame = 0
