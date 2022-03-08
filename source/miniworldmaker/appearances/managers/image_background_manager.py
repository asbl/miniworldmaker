from miniworldmaker.appearances.managers import image_manager

class ImageBackgroundManager(image_manager.ImageManager):

    def __init__(self, appearance):
        super().__init__(appearance)
    
    async def next_image(self):
        """Switches to the next image of the appearance."""
        await super().next_image()
        if self.appearance.is_animated:
            self.repaint_background()

    def set_image_index(self, value) -> bool:
        rvalue = super().set_image_index(value)
        self.repaint_background()
        return rvalue

    def repaint_background(self): 
        self.appearance.parent.app.window.surface.blit(self.appearance.image, (0, 0))
        self.appearance.parent.app.window.add_display_to_repaint_areas()
        self.appearance.parent.view_handler.full_repaint()