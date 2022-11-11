from miniworldmaker.tokens.token_plugins.sensors import sensor
from miniworldmaker.tokens.token_plugins.shapes import shapes


class CircleSensor(sensor.Sensor):
    def _get_sensor(self) -> "shapes.Circle":
        return shapes.Circle(self.token.center)

    @property
    def radius(self):
        return self.sensor.radius

    @radius.setter
    def radius(self, value):
        self.sensor.radius = value
