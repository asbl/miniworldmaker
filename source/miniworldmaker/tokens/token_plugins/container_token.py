from typing import List

import miniworldmaker.tokens.token as token_mod


class ContainerToken(token_mod.Token):
    def __init__(self, children=[]):
        super().__init__()
        self._visible: bool = True
        self._layer: int = 0
        self.children: List["token_mod.Token"] = children

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        self._visible = value
        for child in self.children:
            child.visible = value
        self.dirty = 1

    def add_child(self, token: "token_mod.Token"):
        self.children.append(token)
        token.layer = self.layer + 1

    def remove_child(self, token: "token_mod.Token"):
        self.children.remove(token)

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, value: int):
        self.set_layer(value)

    def set_layer(self, value):
        actual_layer = self.board.tokens.get_layer_of_sprite(self)
        self._layer = value
        if self in self.board.tokens.get_sprites_from_layer(actual_layer):
            self.board._tokens.change_layer(self, value)
        for child in self.children:
            child.layer = self.layer + 1
        self.dirty = 1

    def set_board(self, new_board):
        super().set_board(new_board)
        for child in self.children:
            child.set_board(new_board)

    def reset_costumes(self):
        super().reset_costumes()
        for child in self.children:
            child.reset_costumes()
