from typing import Union, Tuple

from miniworldmaker.tokens import token as token_mod


class Sensor(token_mod.Token):
    """A sensors attached to a token.

    The sensors is not visible and will not detect the token itself.
    """
    def __init__(self, token: "token_mod.Token", relative_position=Union["position_mod.Position", Tuple[float, float]]):
        super().__init__(token.position)
        self.token = token
        self.relative_position = relative_position
        self.visible = False

    def act(self):
        self.center = self.token.center + self.relative_position

    def set_physics_default_values(self):
        """Overwrites method in superclass - The sensors won't be simulated by physics engine.
        """
        self.physics.simulation = None

    def detect_all(self):
        """Detects all token (but not self.token)
        """
        tokens = super().detect_all()
        if self.token in tokens:
            tokens.remove(self.token)
        return tokens

    def detect(self):
        """detects first token (but not self.token)"""
        tokens = self.detect_all()
        if tokens:
            return tokens[0]
        else:
            return None
