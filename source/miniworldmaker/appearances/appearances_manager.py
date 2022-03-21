from miniworldmaker.appearances import appearance
from miniworldmaker.appearances import costume
from miniworldmaker.exceptions import miniworldmaker_exception
from typing import Union, List, Tuple
import pygame
import miniworldmaker

class AppearancesManager:
    def __init__(self, parent, appearance = None):
        if appearance != None:
            self.appearances_list = [appearance]
        else:
            self.appearances_list = []
        self.parent = parent
        self.appearance = appearance
        self._rect = None
        self.is_rotatable = None
        self.is_animated = None
        self.animation_speed = 10
        self.is_upscaled = None
        self.is_scaled = None
        self.is_scaled_to_width = None
        self.is_scaled_to_height = None
        self.has_costume = False

    @property
    def image(self):
        if self.appearance:
            return self.appearance.image
        else:
            return pygame.Surface((1, 1))

    def add_new_appearance(self, appearance, source):
        if source:
            default = False
        else:
            default = True
            if appearance:
                source = appearance._fill_color
        appearance.add_image(source)
        if appearance:
            if default:
                self.add_default(appearance)
            else:
                self.add(appearance)

    def add_default(self, appearance):
        self._add(appearance)

    def add(self, appearance):
        if not self.has_costume:
            self.has_costume = True
            if self.appearances_list:
                first = self.appearances_list.pop(-1)
                del first

        self._add(appearance)

    def _add(self, appearance):
        self.appearances_list.append(appearance)
        if self.is_rotatable is not None:
            appearance.is_rotatable = self.is_rotatable
        if self.is_animated is not None:
            appearance.is_animated = self.is_animated
        if self.animation_speed is not None:
            appearance.animation_speed = self.animation_speed
        if self.is_upscaled is not None:
            appearance.is_upscaled = self.is_upscaled
        if self.is_scaled_to_width is not None:
            appearance.is_scaled_to_width = self.is_scaled_to_width
        if self.is_scaled_to_height is not None:
            appearance.is_scaled_to_height = self.is_scaled_to_height
        if self.is_scaled is not None:
            appearance.is_scaled = self.is_scaled

    def remove(self, index):
        del self.appearances_list[index]

    def get_appearance_at_index(self, appearance: appearance.Appearance) -> int:
        return self.appearances_list.index(appearance)

    def next(self, appearance):
        index = self.get_appearance_at_index(self.costume)
        if index < self.length() - 1:
            index += 1
        else:
            index = 0

    def length(self):
        return len(self.appearances_list)

    def get_appearance_at_index(self, index) -> "appearance.Appearance":
        return self.appearances_list[index]

    def _set_all(self, attribute, value):
        for appearance in self.appearances_list:
            setattr(appearance, attribute, value)

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

    def list(self):
        return self.appearances_list

    def __str__(self):
        return str(len(self.appearances_list)) + " Appearances: " + str(self.appearances_list)

    def remove_appearance(self, appearance=None):
        """Removes a costume from token

        Args:
            index: The index of the new costume. Defaults to -1 (last costume)
        """
        if appearance != None:
            index = self.costumes.get_appearance_at_index_of_costume(appearance)
            self.costumes.remove(index)
        else:
            self.costumes.remove(-1)

    def switch_appearance(self, source: Union[int, "appearance.Appearance"]) -> "costume.Costume":
        if type(source) == int:
            if source >= self.length():
                raise miniworldmaker.CostumeOutOfBoundsError(self.token, self.length(), source)
            new_appearance = self.get_appearance_at_index(source)
        elif isinstance(source, appearance.Appearance):
            new_appearance = source
        self.appearance = new_appearance
        self.appearance.image_manager.end_animation(new_appearance)
        self.appearance.dirty = 1
        return self.appearance

    def animate(self, speed):
        self.appearance.animation_speed = speed
        self.appearance.animate()

    def animate_appearance(self, appearance, speed):
        if appearance is None:
            raise miniworldmaker.CostumeIsNoneError()
        self.switch_appearance(appearance)
        self.costume.animation_speed = speed
        self.costume.animate()

    def self_remove(self):
        pass