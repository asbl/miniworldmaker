from typing import Union, Tuple, List, Optional, Type

import miniworldmaker.tokens.token as token_mod


class Sensor:
    """A sensors attached to a token.

    The sensors is not visible and will not detect the token itself.
    """

    def __init__(self, token: "token_mod.Token", position=Union["position_mod.Position", Tuple[float, float]]):
        self.token = token
        self.token.children.append(self)
        self.sensor = self._get_sensor_class()(self.token.center)
        self.sensor.sensor_position = position
        self.sensor.__sensor_token = token
        self.sensor.visible = False
        if hasattr(self.sensor, "physics"):
            self.sensor.physics.simulation = None
        sensor = self.sensor
        # Register act Method to sensor-Object
        @sensor.register
        def act(self):
            if not self.__sensor_token:
                self.remove()
            else:
                self.center = self.__sensor_token.center + self.sensor_position

    def set_position(self, position):
        """
        Sets the position of the sensor object

        Args:
            position: The position where the sensor should be placed.
        """
        self.sensor.position = position

    def remove(self):
        """ Removes sensor and sensor class
        """
        self.sensor.remove()
        del self

    @property
    def size(self):
        return self.sensor.size

    @size.setter
    def size(self, value):
        self.sensor.size = value

    @property
    def visible(self):
        return self.sensor.size

    @visible.setter
    def visible(self, value):
        self.sensor.visible = value

    def _get_sensor_class(self) -> Type["token_mod.Token"]:
        return token_mod.Token

    def detect_all(self) -> List["token_mod.Token"]:
        """Detects all token (but not self.token)
        """
        tokens = self.sensor.detect_all()
        if self.token in tokens:
            tokens.remove(self.token)
        return tokens

    def detect(self) -> Optional["token_mod.Token"]:
        """detects first token (but not self.token)"""
        tokens = self.detect_all()
        if tokens:
            return tokens[0]
        else:
            return None
