from typing import Union, List, cast

import miniworldmaker.appearances.appearance as appearance_mod
import miniworldmaker.appearances.appearances_manager as appearances_manager
import miniworldmaker.appearances.costume as costume_mod
import miniworldmaker.tokens.token as token_mod


class CostumesManager(appearances_manager.AppearancesManager):

    @property
    def token(self) -> "token_mod.Token":
        return self.parent

    @token.setter
    def token(self, value: "token_mod.Token"):
        self.parent = value

    def get_costume_at_index(self, index):
        return super().get_appearance_at_index(index)

    def add_new_appearance(self,
                           source: Union[str, List[str], "appearance_mod.Appearance"] = None) -> "costume_mod.Costume":
        """
        Adds a new costume to token.
        The costume can be switched with self.switch_costume(index)

        Args:
            source: Path to the first image of new costume

        Returns:
            The new costume.

        """
        new_costume = super().add_new_appearance(source)
        self.appearance.set_dirty("all", self.appearance.LOAD_NEW_IMAGE)
        return cast("costume.Costume", new_costume)

    def create_appearance(self) -> "costume_mod.Costume":
        """Creates a new costume 

        Returns:
            _type_: _description_
        """
        new_costume = self.token.new_costume()
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

    def next_costume(self) -> "costume_mod.Costume":
        return cast("costume.Costume", self.next_appearance())



    def _add_appearance_to_manager(self, appearance):
        return super()._add_appearance_to_manager(appearance)

    def get_board(self):
        return self.token.board

    def remove_from_board(self):
        for costume in self.appearances_list:
            costume.parent = None
            costume.token = None
            del costume