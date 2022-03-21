from miniworldmaker.appearances import appearance
from typing import Union, List, Tuple
from miniworldmaker.appearances import appearances_manager
from miniworldmaker.appearances import costume


class CostumesManager(appearances_manager.AppearancesManager):
    @property
    def costume(self):
        return self.appearance

    @costume.setter
    def costume(self, value):
        self.appearance = value

    @property
    def token(self):
        return self.parent

    @token.setter
    def token(self, value):
        self.parent = value

    def get_costume_at_index(self, index):
        return super().get_appearance_at_index(index)

    def add_costume(self, source: Union[str, List[str], "appearance.Appearance"] = None) -> "costume.Costume":
        """
        Adds a new costume to token.
        The costume can be switched with self.switch_costume(index)

        Args:
            path: Path to the first image of new costume

        Returns:
            The new costume.

        """
        new_costume = costume.Costume(self.token)
        self.costume = new_costume
        self.add_new_appearance(new_costume, source)
        self.costume.update_shape()
        self.costume.dirty = 1
        return new_costume

    @property
    def costumes(self):
        return self.appearances_list

    def switch_costume(self, source):
        self.switch_appearance(source)

    def animate_costume(self, costume, speed):
        super().animate_appearance(costume, speed)

