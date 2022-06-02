from typing import Union

import pygame
import miniworldmaker
import miniworldmaker.appearances.appearance as appearance_mod
import miniworldmaker.exceptions.miniworldmaker_exception as miniworldmaker_exception


class AppearancesManager:
    def __init__(self, parent, appearance=None):
        if appearance is not None:
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
        self.has_appearance = False

    @property
    def image(self):
        if self.appearance:
            return self.appearance.image
        else:
            return pygame.Surface((1, 1))

    def add_new_appearance(self, source):
        """Adds a new Appearance (costume or background) to manager.

        called by ``add_costume`` and ``add_background`` in subclasses.
        """
        if not self.has_appearance and not source:
            return self._add_default_appearance()
        elif not self.has_appearance and source:
            self.has_appearance = True
            return self._add_first_appearance(source)
        else:
            appearance = self.get_default_appearance()
            appearance.add_image(source)
            return self._add_appearance_to_manager(appearance)

    def _add_first_appearance(self, source):
        if self.appearances_list:
            first = self.appearances_list.pop(-1)
            del first
        appearance = self.get_default_appearance()
        appearance.add_image(source)
        self._add_appearance_to_manager(appearance)
        return appearance

    def _add_default_appearance(self):
        appearance = self.get_default_appearance()
        self._add_appearance_to_manager(appearance)
        return appearance

    def _add_appearance_to_manager(self, appearance):
        self.appearance = appearance
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
        return appearance

    def remove(self, index):
        del self.appearances_list[index]

    def next_appearance(self):
        index = self.get_index_for_appearance(self.appearance)
        if index < self.length() - 1:
            index += 1
        else:
            index = 0
        return self.switch_appearance(index)

    def length(self):
        return len(self.appearances_list)

    def get_appearance_at_index(self, index) -> "appearance_mod.Appearance":
        return self.appearances_list[index]

    def get_index_for_appearance(self, appearance):
        for index, a_appearance in enumerate(self.appearances_list):
            if a_appearance == appearance:
                return index

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

    def _remove_appearance_at_index(self, index):
        appearance = self.get_appearance_at_index(index)
        self._remove_appearance_from_manager(appearance)

    def _remove_appearance_from_manager(self, appearance):
        if self.has_appearance and self.count():
            if appearance == self.appearance:
                index = self.get_index_for_appearance(appearance)
                if index == 0:
                    self.has_costume = False
                    self._add_default_appearance()
                self.switch_appearance(self.get_appearance_at_index(index - 1))
            self.appearances_list.remove(appearance)

    def remove_appearance(self, source: Union[int, "appearance_mod.Appearance"] = -1):
        """Removes an appearance (costume or background) from manager

        Defaults:
            Removes last costume.

        Args:
            source: The index of the new appearance or the Appearance which should be removed Defaults to -1
            (last costume)
        """
        if type(source) == int:
            self._remove_appearance_at_index(source)
        elif isinstance(source, appearance_mod.Appearance):
            self._remove_appearance_from_manager(source)

    def switch_appearance(self, source: Union[int, "appearance_mod.Appearance"]) -> "appearance_mod.Appearance":
        if type(source) == int:
            if source >= self.length():
                raise miniworldmaker_exception.CostumeOutOfBoundsError(self.parent, self.length(), source)
            new_appearance = self.get_appearance_at_index(source)
        elif isinstance(source, appearance_mod.Appearance) or isinstance(source, miniworldmaker.Appearance):
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
            raise miniworldmaker_exception.CostumeIsNoneError()
        self.switch_appearance(appearance)
        self.costume.animation_speed = speed
        self.costume.animate()

    def self_remove(self):
        """Implemented in subclasses"""
        pass

    def count(self):
        if self.has_appearance:
            return len(self.appearances_list)
        else:
            return 0
