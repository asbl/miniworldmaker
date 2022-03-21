from miniworldmaker.appearances.managers import image_manager


class ImageBackgroundManager(image_manager.ImageManager):
    def __init__(self, appearance):
        super().__init__(appearance)

    async def next_image(self):
        """Switches to the next image of the appearance."""
        await super().next_image()
        if self.appearance.is_animated:
            self.appearance.repaint_background()

    def set_image_index(self, value) -> bool:
        rvalue = super().set_image_index(value)
        self.appearance.repaint_background()
        return rvalue

    def _add_scaling(self, source):
        self.appearance.is_scaled = True
