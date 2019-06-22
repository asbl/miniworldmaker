import math

import pymunk as pymunk_engine
import pymunk.pygame_util


class PhysicsProperty:

    space = None
    gravity_x = 0
    gravity_y = -900
    count = 0

    def __init__(self, token, can_move, box_type, gravity, mass, friction, elasticity, size, stable):
        if not PhysicsProperty.space:
            PhysicsProperty.space = pymunk_engine.Space()
            PhysicsProperty.space.gravity = PhysicsProperty.gravity_x, PhysicsProperty.gravity_y
            PhysicsProperty.space.iterations = 35
            PhysicsProperty.space.damping = 0.9
            PhysicsProperty.space.collision_persistence = 10
            pymunk.pygame_util.positive_y_is_up = True
        self.token = token
        self.gravity = gravity
        self.mass = mass
        self.can_move = can_move
        self._stable = stable
        self._velocity_x = 0
        self._velocity_y = 0
        self.box_type = box_type
        self.body = None
        self.elasticity = elasticity
        self.friction = friction
        self.dirty = 0
        self.size = size
        PhysicsProperty.count += 1
        self._make_pymunk()

    def update_physics_model(self):
        if self.dirty:
            self.space.remove(self.body.shapes)
            self.space.remove(self.body)
            self._make_pymunk()
        if not self.body.body_type == pymunk_engine.Body.STATIC:
            self.body.position = pymunk.pygame_util.from_pygame((self.token.center_x,
                                                                 self.token.center_y),
                                                                self.token.board.image)
            PhysicsProperty.space.reindex_shapes_for_body(self.body)
            self.body.angle = (math.radians(round(self.token.direction_at_unit_circle, 0)))

    def update_token_from_physics_model(self):
        if not self.body.body_type == pymunk_engine.Body.STATIC:
            b_x, b_y = self.body.velocity
            if b_x > -1 and b_x < 1:
                self.velocity_x = 0
            if b_y > -1 and b_y < 1:
                self.velocity_y = 0
            self.token.center_x, self.token.center_y = pymunk.pygame_util.to_pygame(self.body.position, self.token.board.image)
            self.token.direction_at_unit_circle = int(math.degrees(self.body.angle))
            a_x, a_y = self.body.velocity
        #options = pymunk.pygame_util.DrawOptions(self.token.board.image)
        #options.collision_point_color = (255, 20, 30, 40)
        #PhysicsProperty.space.debug_draw(options)

    def _make_pymunk(self):
        if self.token.position != None:
            # mass
            mass = self.mass

            # Body (dynamic, static or kinematic
            if self.can_move and not self.stable:
                body_type = pymunk_engine.Body.DYNAMIC
            elif self.can_move and self.stable:
                if self.gravity:
                    body_type = pymunk_engine.Body.DYNAMIC
                else:
                    body_type = pymunk_engine.Body.KINEMATIC
            else:
                body_type = pymunk_engine.Body.STATIC
            if self.stable:
                moment = pymunk.inf
            elif self.box_type == "circle":
                moment = pymunk_engine.moment_for_circle(mass, 0, self.size[0] * self.token.width/2, (0, 0))
            else:
                moment = pymunk_engine.moment_for_box(mass = mass, size=(self.token.width, self.token.height))

            # create body
            self.body = pymunk_engine.Body(mass=mass,moment=moment, body_type=body_type)
            if self.box_type == "rect":
                shape = pymunk.Poly.create_box(self.body, (self.size[0] * self.token.width, self.size[1] * self.token.height))
            else:
                shape = pymunk.Circle(self.body, self.size[0] * self.token.width/2, (0, 0))
            self.body.position = pymunk.pygame_util.from_pygame((self.token.center_x, self.token.center_y), self.token.board.image)
            self.body.friction = self.friction
            shape.elasticity = self.elasticity
            PhysicsProperty.space.add(self.body, shape)
            self.dirty = 0
        else:
            self.debug = True

    @property
    def velocity_x(self):
        return self._velocity_x

    @velocity_x.setter
    def velocity_x(self, value):
        self._velocity_x = value
        self.body.velocity = value, self.body.velocity[1]

    @property
    def velocity_y(self):
        return self._velocity_y

    @velocity_y.setter
    def velocity_y(self, value):
        self._velocity_y = value
        self.body.velocity = self.body.velocity[0], value

    @property
    def stable(self):
        return self._stable

    @stable.setter
    def stable(self, value):
        self.stable = value
        self.dirty = 1

    def impuls(self, impulse, point):
        self.body.apply_impulse_at_local_point(impulse, point)
