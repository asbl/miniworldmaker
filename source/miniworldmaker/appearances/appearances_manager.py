from typing import Union, Tuple, List

import pygame

import miniworldmaker
import miniworldmaker.appearances.appearance as appearance_mod
import miniworldmaker.exceptions.miniworldmaker_exception as miniworldmaker_exception
import miniworldmaker.appearances.costume as costume
from miniworldmaker.exceptions.miniworldmaker_exception import MiniworldMakerError


class AppearancesManager:
    def __init__(self, parent):
        self.appearances_list = []
        self.parent = parent
        self.appearance = None
        self._rect = None
        self.is_rotatable = None
        self.is_animated = None
        self.animation_speed = 10
        self.is_upscaled = None
        self.is_scaled = None
        self.is_scaled_to_width = None
        self.is_scaled_to_height = None
        self.has_appearance = False
        self._iter_index = 0

    @property
    def image(self) -> pygame.Surface:
        if self.appearance:
            return self.appearance.image
        else:
            return pygame.Surface((1, 1))

    def _create_appearance_from_source(self, source) -> "appearance_mod.Appearance":
        if isinstance(source, costume.Costume):
            return source
        if source is None:
            appearance = self.create_appearance()
        elif type(source) in [str, pygame.Surface, tuple]:
            appearance = self.create_appearance()
            appearance.add_image(source)
        else:
            raise MiniworldMakerError(f"Wrong type in _create_appearance_from_source got {type(source)}", )
        return appearance

    def add_new_appearance(
            self, source: Union[str, pygame.Surface, "costume.Costume", Tuple, None]
    ) -> "appearance_mod.Appearance":
        """Adds a new Appearance (costume or background) to manager.

        called by ``add_costume`` and ``add_background`` in subclasses.
        """
        appearance: "appearance_mod.Appearance" = self._create_appearance_from_source(source)
        if not self.has_appearance and source:
            self.has_appearance = True
            return self._add_first_appearance(appearance)
        elif not self.has_appearance and not source:
            self.has_appearance = False
            return self._add_default_appearance()
        elif source:
            return self._add_appearance_to_manager(appearance)
        else:
            raise MiniworldMakerError(
                f"""Error: Got wrong type for appearance. 
                Expected: str, pygame.Surface, Costume, tuple;  got {type(source)}, {source}"""
            )

    def set_new_appearance(
            self, source: Union[str, pygame.Surface, "costume.Costume", Tuple, None]):
        if not self.has_appearance:
            return self.add_new_appearance(source)
        else:
            self.remove_appearance()
            self.add_new_appearance(source)
    def add_new_appearances(self, sources: List) -> None:
        if type(sources) in [list]:
            for appearance in sources:
                self.add_new_appearance(appearance)
        else:
            raise MiniworldMakerError(f"Appearances must be list, got {type(sources)}")

    def add_new_appearance_from_list(self, sources: List) -> "appearance_mod.Appearance":
        head = sources[0]
        tail = sources[1:]
        appearance = self.add_new_appearance(head)
        for source in tail:
            appearance.add_image(source)
        return appearance

    def create_appearance(self) -> "appearance_mod.Appearance":
        """Returns a new appearance (Background instance or Costume instance)"""
        pass

    def _add_default_appearance(self) -> "appearance_mod.Appearance":
        appearance = self.create_appearance()
        return self._add_first_appearance(appearance)

    def _add_first_appearance(self, appearance: "appearance_mod.Appearance") -> "appearance_mod.Appearance":
        self.appearances_list = []
        self._add_appearance_to_manager(appearance)
        return appearance

    def _add_appearance_to_manager(self, appearance: "appearance_mod.Appearance") -> "appearance_mod.Appearance":
        self.appearance = appearance
        self.appearances_list.append(appearance)
        appearance.set_defaults(self.is_rotatable, self.is_animated, self.animation_speed, self.is_upscaled,
                                self.is_scaled_to_width, self.is_scaled_to_height, self.is_scaled, self.is_flipped, self.border)
        self.appearance.set_dirty("all", self.appearance.LOAD_NEW_IMAGE)
        return appearance

    def next_appearance(self) -> "appearance_mod.Appearance":
        """Switches to next appearance

        Returns:
            appearance_mod.Appearance: the switched appearance
        """
        index = self.find_appearance(self.appearance)
        if index < self.length() - 1:
            index += 1
        else:
            index = 0
        return self.switch_appearance(index)

    def length(self) -> int:
        """Number of appearance in appearance manager

        Returns:
            int: _description_
        """
        if self.has_appearance:
            return len(self.appearances_list)
        else:
            return 0

    def __len__(self) -> int:
        return self.length()

    def get_appearance_at_index(self, index: int) -> Union["appearance_mod.Appearance", None]:
        if 0 <= index < len(self.appearances_list):
            return self.appearances_list[index]
        else:
            return None

    def find_appearance(self, appearance: "appearance_mod.Appearance") -> int:
        """Searches for appearance; returns index of appearance

        Returns:
            int: Index of found appearance; -1 if appearance was not found.
        """
        for index, a_appearance in enumerate(self.appearances_list):
            if a_appearance == appearance:
                return index
        return -1

    def _set_all(self, attribute, value):
        """Sets attribute for all appearance in manager."""
        for appearance in self.appearances_list:
            setattr(appearance, attribute, value)

    def set_border(self, value):
        self.is_animated = value
        self._set_all("border", value)

    def set_animated(self, value):
        self.is_animated = value
        self._set_all("is_animated", value)

    def set_animation_speed(self, value):
        self.animation_speed = value
        self._set_all("animation_speed", value)

    def set_rotatable(self, value):
        self.is_rotatable = value
        self._set_all("is_rotatable", value)

    def set_upscaled(self, value):
        self.is_upscaled = value
        self._set_all("is_upscaled", value)

    def set_scaled_to_width(self, value):
        self.is_scaled_to_width = value
        self._set_all("is_scaled_to_width", value)

    def set_scaled_to_height(self, value):
        self.is_scaled_to_height = value
        self._set_all("is_scaled_to_height", value)

    def set_scaled(self, value):
        self.is_scaled = value
        self._set_all("is_scaled", value)

    def list(self) -> List[appearance_mod.Appearance]:
        """Returns all appearances in manager as list.

        Returns:
            List[appearance_mod.Appearance]: All appearances in manager as list
        """
        return self.appearances_list

    def __str__(self):
        return str(len(self.appearances_list)) + " Appearances: " + str(self.appearances_list)

    def _remove_appearance_from_manager(self, appearance: "appearance_mod.Appearance"):
        """Removes appearance from manager

        If length == 1, default appearance will be added.
        """
        if self.has_appearance and self.length() > 0:
            if appearance == self.appearance:
                if self.length() == 1:
                    self.appearances_list.remove(appearance)
                    del appearance
                    self._add_default_appearance()
                    self.has_appearance = False
                else:
                    first_appearance = self.get_appearance_at_index(0)
                    self.switch_appearance(first_appearance)
                    self.appearances_list.remove(appearance)
                    del appearance

    def remove_appearance(self, source: Union[int, "appearance_mod.Appearance"] = -1):
        """Removes an appearance (costume or background) from manager

        Defaults:
            Removes last costume.

        Args:
            source: The index of the new appearance or the Appearance which should be removed Defaults to -1
            (last costume)
        """
        if type(source) == int:
            source = self.get_appearance_at_index(source)
        if source and isinstance(source, appearance_mod.Appearance):
            self._remove_appearance_from_manager(source)
        else:
            raise MiniworldMakerError(f"Expected type int or Appearance (Costume or Background), got {type(source)}")

    def reset(self):
        for appearance in self.appearances_list:
            self.remove_appearance(appearance)

    def switch_appearance(self, source: Union[int, "appearance_mod.Appearance"]) -> "appearance_mod.Appearance":
        if type(source) == int:
            if source >= self.length():
                raise miniworldmaker_exception.CostumeOutOfBoundsError(self.parent, self.length(), source)
            new_appearance = self.get_appearance_at_index(source)
        elif isinstance(source, appearance_mod.Appearance) or isinstance(source, miniworldmaker.Appearance):
            new_appearance = source
        else:
            raise MiniworldMakerError(f"Wrong type in switch_appearance, got {type(source)}")
        self.appearance = new_appearance
        self.appearance.image_manager.end_animation(new_appearance)
        self.appearance.set_image(0)
        self.appearance.set_dirty("all", self.appearance.LOAD_NEW_IMAGE)
        return self.appearance

    def animate(self, speed: int):
        self.appearance.animation_speed = speed
        self.appearance.animate()

    def get_board(self):
        """Implemented in subclasses
        """
        pass

    def animate_appearance(self, appearance: "appearance_mod.Appearance", speed: int):
        if appearance is None:
            raise miniworldmaker_exception.CostumeIsNoneError()
        self.switch_appearance(appearance)
        self.appearance.animation_speed = speed
        self.appearance.animate()

    def self_remove(self) -> None:
        """Implemented in subclasses"""
        pass

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index < len(self.appearances_list):
            appearance_at_position = self.get_appearance_at_index(self._iter_index)
            self._iter_index += 1
            return appearance_at_position
        else:
            raise StopIteration

    @property
    def orientation(self):
        return [appearance.orientation for appearance in self.appearances_list]

    @orientation.setter
    def orientation(self, value):
        for appearance in self.appearances_list:
            appearance.orientation = value

    @property
    def animation_speed(self):
        return self.appearance.animation_speed

    @animation_speed.setter
    def animation_speed(self, value):
        for appearance in self.appearances_list:
            appearance.animation_speed = value

    @property
    def is_flipped(self):
        return self.appearance.is_flipped

    @is_flipped.setter
    def is_flipped(self, value):
        for appearance in self.appearances_list:
            appearance.is_flipped = value

    @property
    def border(self):
        return self.appearance.border

    @border.setter
    def border(self, value):
        for appearance in self.appearances_list:
            appearance.border = value

    def get_actual_appearance(self):
        return self.appearance

