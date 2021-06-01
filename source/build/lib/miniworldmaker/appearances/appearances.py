class Appearances:
    def __init__(self, appearance):
        self.appearances = [appearance]
        self.is_rotatable = None
        self.is_animated = None
        self.animation_speed = None
        self.is_upscaled = None
        self.is_scaled = None
        self.is_scaled_to_width = None
        self.is_scaled_to_height = None

    def add(self, appearance):
        self.appearances.append(appearance)
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

    def get_position_of(self, appearance):
        return self.appearances.index(appearance)

    def len(self):
        return len(self.appearances)

    def get_at_position(self, index):
        return self.appearances[index]

    # def _do_all(self, method, parameters):
    #    for appearance in self.appearances:
    #        if parameters is None:
    #            method()
    #        else:
    #            method(parameters)

    def _set_all(self, attribute, value):
        for appearance in self.appearances:
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
        return self.appearances


class Costumes(Appearances):
    def set_flip_vertical(self, value):
        self._set_all("flip_vertical", value)
