
from typing import Union, List, Tuple
import miniworldmaker.appearances. appearances_manager as appearances_manager
import miniworldmaker.appearances.costume as costume
import miniworldmaker.appearances.appearance as appearance


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
        new_costume = self.add_new_appearance(source)
        self.costume._update_shape()
        self.costume.dirty = 1
        return new_costume

    def get_default_appearance(self):
        new_costume = costume.Costume(self.token)
        return new_costume

    @property
    def costumes(self):
        return self.appearances_list

    def switch_costume(self, source):
        self.switch_appearance(source)

    def animate_costume(self, costume, speed):
        super().animate_appearance(costume, speed)

    @property
    def has_costume(self):
        return self.has_appearance

    @has_costume.setter
    def has_costume(self, value):
        self.has_appearance = value