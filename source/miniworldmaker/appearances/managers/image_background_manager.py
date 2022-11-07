import miniworldmaker.appearances.managers.image_manager as image_manager


class ImageBackgroundManager(image_manager.ImageManager):
    def __init__(self, appearance):
        super().__init__(appearance)

    def next_image(self):
        """Switches to the next image of the appearance."""
        # was next_image()
        super().next_image()
        if self.appearance.is_animated:
            self.appearance._blit_to_window_surface()

    def set_image_index(self, value) -> bool:
        rvalue = super().set_image_index(value)
        self.appearance._blit_to_window_surface()
        return rvalue

    def _add_scaling(self, source):
        self.appearance.is_scaled = True
