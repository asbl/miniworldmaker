from miniworldmaker.appearances.managers import image_manager

class ImageBoardManager(image_manager.ImageManager):
    
    async def next_image(self, appearance):
        """Switches to the next image of the appearance."""
        super().next_image(appearance)
        if appearance.is_animated:
            self.repaint_background(appearance)

    def set_image_index(self, value, appearance) -> bool:
        rvalue = super().set_image_index(value, appearance)
        self.repaint_background(appearance)
        return rvalue

    def repaint_background(self, appearance): 
        appearance.parent.app.window.surface.blit(appearance.image, (0, 0))
        appearance.parent.app.window.add_display_to_repaint_areas()
        appearance.parent.view_handler.full_repaint()