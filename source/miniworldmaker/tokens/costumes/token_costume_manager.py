from typing import Union, Type, TypeVar, List
from miniworldmaker.appearances import appearances
from miniworldmaker.appearances import appearance
from miniworldmaker.appearances import costume
from miniworldmaker.exceptions.miniworldmaker_exception import CostumeIsNoneError, CostumeOutOfBoundsError


class TokenCostumeManager:
    def __init__(self, token, image):
        self.token = token
        self._rect = None
        self.costume = None
        self.costumes = appearances.Costumes(self.costume)
        self._dirty = 1
        self.has_costume = False
        if image is not None:
            self.add_costume(image)
            self.has_costume = True
        else:
            self.add_costume(None)
            self.has_costume = False

    @property
    def image(self):
        if self.costume:
            return self.costume.image
        else:
            return None

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value
        if hasattr(self.token, "board") and self.token.board:
            self.token.board.dirty = 1

    def add_costume(self, source: Union[str, List[str], "appearance.Appearance"] = (255, 255, 0, 0)) -> costume.Costume:
        """
        Adds a new costume to token.
        The costume can be switched with self.switch_costume(index)

        Args:
            path: Path to the first image of new costume

        Returns:
            The new costume.

        """
        if not self.has_costume and self.costume != None:
            self.remove_costume()
        if source is None:
            source = (255, 0, 255, 100)
        new_costume = costume.Costume(self.token)
        if type(source) == str:
            new_costume.add_image(source)
            if not self.token.__class__.class_image:
                self.__class__.class_image = source
        if type(source) == list:
            for image in source:
                new_costume.add_image(image)
        elif type(source) == tuple:
            new_costume.fill_color = source
        if self.costume is None or not self.has_costume:
            self.costume = new_costume
            self.has_costume = True
        self.costumes.add(new_costume)
        self.dirty = 1
        return new_costume

    def remove_costume(self, costume=None):
        """Removes a costume from token

        Args:
            index: The index of the new costume. Defaults to -1 (last costume)
        """
        if costume != None:
            index = self.costumes.get_index_of_costume(costume)
            self.costumes.remove(index)
        else:
            self.costumes.remove(-1)

    def switch_costume(self, costume: Union[int, "appearance.Appearance"]) -> costume.Costume:
        """Switches the costume of token

        Args:
            next: If next is True, the next costume will be selected

        Returns: The new costume
        """
        if type(costume) == int:
            if costume >= self.costumes.count_costumes():
                raise CostumeOutOfBoundsError(self.token, self.costumes.count_costumes, costume)
            costume = self.costumes.get_costume_at_index(costume)
        self.costume.end_animation()  # ? neccessary
        self.costume = costume
        self.costume.dirty = 1
        return self.costume

    def next_costume(self):
        """Switches to the next costume of token

        Args:
            next: If next is True, the next costume will be selected

        Returns: The new costume
        """
        self.costume.end_animation()
        index = self.costumes.get_index_of_costume(self.costume)
        if index < self.costumes.len() - 1:
            index += 1
        else:
            index = 0

    def rotate_costume(self):
        self.dirty = 1
        if self.costume:
            self.costume.call_action("rotate")
        if self.token.board:
            self.token.board.app.event_manager.send_event_to_containers(
                "token_changed_direction", self)

    def resize_costume(self):
        if self.costume:
            self.costume._reload_all()

    def flip_costume(self, value):
        self.costume.is_flipped = value

    def animate(self, speed):
        self.costume.animation_speed = speed
        self.costume.animate()

    def animate_costume(self, costume, speed):
        if costume is None:
            raise CostumeIsNoneError()
        self.switch_costume(costume)
        self.costume.animation_speed = speed
        self.costume.animate()

    def loop_animation(self, speed):
        self.costume.animation_speed = speed
        self.costume.loop = True
        self.costume.animate()

    def remove(self):
        """
        The method is overwritten in subclasses
        """
        pass

    def get_token_rect(self):
        if self.token.dirty == 1:
            self._rect = self._reload_token_rect_from_costume()
            return self._rect
        else:
            return self._rect

    def reload_costume(self):
        self.costume._reload_all()
