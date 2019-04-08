from tools import appearance


class Background(appearance.Appearance):
    def __init__(self, board):
        super().__init__()
        self.parent = board


    def next_sprite(self):
        super().next_sprite()
        self.parent.window.repaint_areas.append(self.image.get_rect())
        self.parent.window.window_surface.blit(self.image, (0, 0))

    def show_grid(self, color=(255, 255, 255, 255)):
        self.dirty = 1
        self.color = color
        self.enabled_image_actions["grid"] = True
        self.call_action("grid")
