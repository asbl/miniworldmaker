import pymunk as pymunk_engine

class PhysicsProperty:

    space = None
    gravity_x = 0
    gravity_y = 9.81


    def __init__(self, token):
        if not PhysicsProperty.space:
            PhysicsProperty.space = pymunk_engine.Space()
            PhysicsProperty.space.gravity = PhysicsProperty.gravity_x, PhysicsProperty.gravity_y
            PhysicsProperty.space.sleep_time_threshold = 0.5
            PhysicsProperty.space.idle_speed_threshold = 0  # pymunk estimates good threshold based on gravity
        self.token = token
        self.gravity = True
        self.mass = 50
        self.can_move = True
        self.stable = True
        self._velocity_y = 0
        self._velocity_x = 0
        self._pymunk_body = None
        self.speed_x=0
        self.speed_y=0
        self._make_pymunk()

    def update(self):
        PhysicsProperty.space.step(1 / (60.0 * 1))
        if self._pymunk_body != None:
            self.speed_x, self.speed_y = self._pymunk_body.velocity
            self.token.x += self.speed_x
            self.token.y += self.speed_y

    def _make_pymunk(self):
        mass = self.mass

        # Pymunk body
        if self.can_move and not self.stable:
            body_type = pymunk_engine.Body.DYNAMIC
        elif self.can_move and self.stable:
            if self.gravity:
                body_type = pymunk_engine.Body.DYNAMIC
            else:
                body_type = pymunk_engine.Body.KINEMATIC
        else:
            body_type = pymunk_engine.Body.STATIC

        # Pymunk moment
        if self.stable:
            moment = pymunk_engine.inf
        else:
            moment = pymunk_engine.moment_for_box(mass, (self.sprite.width, self.sprite.height))

        self._pymunk_body = pymunk_engine.Body(mass, moment, body_type=body_type)
        self._pymunk_body.velocity = (self.velocity_x, self.velocity_y)

        if not self.gravity:
            self._pymunk_body.velocity_func = lambda body, gravity, damping, dt: None

        self._pymunk_shape = pymunk_engine.Poly.create_box(self._pymunk_body, (self.token.rect.width, self.token.rect.height))
        PhysicsProperty.space.add(self._pymunk_body, self._pymunk_shape)

    @property
    def velocity_x(self):
        return self._velocity_y

    @velocity_x.setter
    def velocity_x(self, value):
        self._velocity_x = value
        self._pymunk_body.velocity =  value, self._pymunk_body.velocity[1]

    @property
    def velocity_y(self):
        return self._velocity_y

    @velocity_y.setter
    def velocity_y(self, value):
        self._velocity_y = value
        self._pymunk_body.velocity = self._pymunk_body.velocity[0], value


