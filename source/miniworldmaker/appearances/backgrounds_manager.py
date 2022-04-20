import miniworldmaker.appearances.appearances_manager as appearances_manager
import miniworldmaker.appearances.background as background


class BackgroundsManager(appearances_manager.AppearancesManager):
    def __init__(self, parent, appearance=None):
        super().__init__(parent, appearance)
        self.repaint_all: int = 1

    @property
    def background(self):
        return self.appearance

    @background.setter
    def background(self, value):
        self.appearance = value

    @property
    def board(self):
        return self.parent

    @board.setter
    def board(self, value):
        self.parent = value

    def get_background_at_index(self, index):
        return super().get_appearance_at_index(index)

    def add_background(self, source):
        new_background = self.add_new_appearance(source)
        return new_background

    def get_default_appearance(self):
        new_background = background.Background(self.board)
        return new_background

    def switch_background(self, source):
        background = super().switch_appearance(source)
        for token in self.board.tokens:
            token.dirty = 1
        return background

    @property
    def backgrounds(self):
        return self.appearances_list

    """
    

    def init_background(self, background_image):
        if background_image is not None:
            self.add_background(background_image)
            self.has_background = True
        else:
            self.add_background(None)
            self.has_background = False


    def switch_background(self, value : Union["appearance.Appearance", int]):
        if type(value) == int:
            background = self.backgrounds.get_background_at_index(value)
        elif type(value) == appearance.Appearance:
            index = self.backgrounds.get_appearance_at_index(value)
        self.background = background
        for token in self.board.tokens:
            token.dirty = 1
        return self.background

    """
