import math

import pygame

import miniworldmaker.appearances.costume as costume


class ShapeCostume(costume.Costume):
    def __init__(self, token):
        super().__init__(token)
        self.set_image((0, 0, 0, 0))

    def _set_token_default_values(self):
        self._info_overlay = False
        self._is_rotatable = True
        self.is_scaled = True
        self.is_upscaled = False
        self.is_filled = True
        self.fill_color = (255, 255, 255, 50)
        self.border_color = (100, 100, 100, 255)
        self.border = 1


class CircleCostume(ShapeCostume):
    def _inner_shape(self):
        return pygame.draw.circle, [(self.parent.size[0] / 2, self.parent.size[0] / 2), self.parent.radius, 0]

    def _outer_shape(self):
        return pygame.draw.circle, [
            (self.parent.size[0] / 2, self.parent.size[0] / 2),
            self.parent.radius,
            self.border,
        ]

    def rotated(self):
        pass  # Do not set dirty after rotation


class EllipseCostume(ShapeCostume):
    def _inner_shape(self):
        return pygame.draw.ellipse, [pygame.Rect(0, 0, self.parent.size[0], self.parent.size[1]), 0]

    def _outer_shape(self):
        return pygame.draw.ellipse, [pygame.Rect(0, 0, self.parent.size[0], self.parent.size[1]), self.border]


class ArcCostume(ShapeCostume):
    def _inner_shape(self):
        p = []
        for n in range(int(self.parent.start_angle), int(self.parent.end_angle), 1):
            x = int(self.parent.size[0] / 2 + self.parent.width / 2 * math.cos(n * math.pi / 180))
            y = int(self.parent.size[1] / 2 - self.parent.height / 2 * math.sin(n * math.pi / 180))
            p.append((x, y))
        p.append((self.parent.size[0] / 2, self.parent.size[1] / 2))
        return pygame.draw.polygon, [p, 0]

    def _outer_shape(self):
        return pygame.draw.arc, [
            pygame.Rect(0, 0, self.parent.size[0], self.parent.size[1]),
            math.radians(self.parent.start_angle),
            math.radians(self.parent.end_angle),
            1,
        ]


class LineCostume(ShapeCostume):
    def __init__(self, token):
        self.local_start_position, self.local_end_position = (0, 0), (0, 0)
        super().__init__(token)

    def _inner_shape(self):
        return pygame.draw.line, [(self.thickness / 2, self.thickness),
                                  (self.thickness / 2, self.token.size[1] - self.thickness), 0]

    def _outer_shape(self):
        return pygame.draw.line, [(self.thickness / 2, self.thickness),
                                  (self.thickness / 2, self.token.size[1] - self.thickness), self.thickness]

    @property
    def thickness(self):
        """-> see border"""
        return int(self.border)

    @thickness.setter
    def thickness(self, value):
        self.border = value


class RectangleCostume(ShapeCostume):
    def _inner_shape(self):
        return pygame.draw.rect, [pygame.Rect(0, 0, self.token.size[0], self.token.size[1]), 0]

    def _outer_shape(self):
        return pygame.draw.rect, [pygame.Rect(0, 0, self.token.size[0], self.token.size[1]), self.border]


class PolygonCostume(ShapeCostume):
    def __init__(self, token, pointlist):
        super().__init__(token)
        self.border = 1

    def _update_draw_shape(self):
        pointlist = self.token.pointlist
        min_x = min([p[0] for p in pointlist])
        min_y = min([p[1] for p in pointlist])
        width = max([p[0] - min_x for p in pointlist]) + self.border
        height = max([p[1] - min_y for p in pointlist]) + self.border
        self.parent.size = (width, height)
        self.mod_pointlist = []
        for point in pointlist:
            x = point[0] - min_x
            y = point[1] - min_y
            self.mod_pointlist.append((x, y))
        self.parent.position = min_x, min_y
        super()._update_draw_shape()

    def _inner_shape(self):
        return pygame.draw.polygon, [self.mod_pointlist, 0]

    def _outer_shape(self):
        return pygame.draw.polygon, [self.mod_pointlist, self.border]
