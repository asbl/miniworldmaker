from typing import Type

import miniworldmaker.tokens.token_plugins.sensors.sensor as sensor
import miniworldmaker.tokens.token_plugins.shapes as shapes


class CircleSensor(sensor.Sensor):
    def _get_sensor(self) -> Type["shapes.Circle"]:
        return shapes.Circle

    @property
    def radius(self):
        return self.sensor.radius

    @radius.setter
    def radius(self, value):
        self.sensor.radius = value
