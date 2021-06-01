import math

import pymunk as pymunk_engine
import pymunk.pygame_util


class PhysicsProperty:
    """
    The PhysicsProperty class describes all properties necessary to physically
    simulate an object using the pymunk engine.

    The properties are defined in the method setup_physics().
    You can override this method if you want your class to have different physical properties.

    For an object to be physically simulated,
    the method start_physics() must first be called.

    Examples:
        >>> class Player(miniworldmaker.Token):
        >>>
        >>> def on_setup(self):
        >>>    pass # setup Object
        >>>
        >>> def setup_physics(self):
        >>>     self.physics.size = (0.8, 0.8)
        >>>     self.physics.shape_type = "circle"

        Creates a Physics Player. By creating the method setup_physics, the object will be run by physics engine.

    Attributes:
        friction (int): Friction is the force resisting the relative motion of solid surfaces,
            fluid layers, and material elements sliding against each other.
            Friction has a value > 0
        elasticity (int): continuum mechanics of bodies that deform reversibly under stress
        mass: The mass of an object. Default: 1
        stable: If True, the Object has no moment and can't be rotated by an impulse
        can_move: Defines if the object can move
        gravity: Defines if the object affected by gravity
        shape_type: line, circle or rect
    """

    space = None
    gravity_x = 0
    gravity_y = -900
    count = 0
    debug = False
    collision_types = list
    accuracy = 1

    def __init__(self):
        if not PhysicsProperty.space:
            PhysicsProperty.space = pymunk_engine.Space()
            PhysicsProperty.space.gravity = PhysicsProperty.gravity_x, PhysicsProperty.gravity_y
            PhysicsProperty.space.iterations = 35
            PhysicsProperty.space.damping = 0.9
            PhysicsProperty.space.collision_persistence = 10
            # pymunk.pygame_util.positive_y_is_up = True
        self.token = None
        self.mass = 1
        self.gravity = True
        self.stable = True
        self.friction = 10
        self.can_move = True
        self._velocity_x = 0
        self._velocity_y = 0
        self.elasticity = 0.5
        self.shape_type = "rect"
        self.body = None
        self.shape = None
        self.correct_angle = 0
        self.dirty = 1
        self.started = False
        self.model_setup_complete = False
        self.size = (1, 1)  # scale factor for physics box model

    def start_physics(self):
        """
        Starts the physcis-simulation for this object. If you want to use Physics-Sumulation with your object,
        you have to use this method.

        WARNING: This method should be called AFTER all changes of attributes but BEFORE you add an impulse to the object
        If you implement a setup_physics()-Method in an token, you don't have to call this method.

        Examples:
            >>> # These attributes are changed BEFORE start_physics()
            >>> self.physics.size = 0.7, 0.7
            >>> self.physics.shape_type = "circle"
            >>> self.physics.stable = False
            >>> # The physics simulation is started
            >>> self.start_physics()
            >>> # The impulse is applied to the object AFTER starting the physics simulation
            >>> self.physics.velocity_x = 1500
            >>> self.physics.velocity_y = - self.board.arrow.direction * 50
        """
        self.started = True
        PhysicsProperty.count += 1

    def setup_physics_model(self):
        if self.dirty and self.token.position:  # if token is on board
            # mass
            if self.mass != "inf":
                mass = self.mass
            else:
                mass = pymunk.inf

            # Sets the body type:
            # dynamic: Influenced by physic (e.g. actors)
            # static: not influenced by physics (e.g. plattforms)
            # kinematic: e.g. moving plattforms
            if self.can_move and not self.stable:
                body_type = pymunk_engine.Body.DYNAMIC
            elif self.can_move and self.stable:
                if self.gravity:
                    body_type = pymunk_engine.Body.DYNAMIC
                else:
                    body_type = pymunk_engine.Body.KINEMATIC
            else:
                body_type = pymunk_engine.Body.STATIC
            # Sets the moment
            # if stable: pymunk.inf: Object won't be rotated by an impulse
            if self.stable:
                moment = pymunk.inf
            elif self.shape_type == "rect":
                moment = pymunk_engine.moment_for_box(mass,
                                                      (self.size[0] * self.token.width,
                                                       self.size[1] * self.token.height,
                                                       ),
                                                      )
            elif self.shape_type == "circle":
                moment = pymunk_engine.moment_for_circle(mass, 0, self.size[0] * self.token.width / 2, (0, 0))
            elif self.shape_type == "line":
                moment = pymunk_engine.moment_for_segment(mass,
                                                          pymunk.pygame_util.from_pygame(self.token.start_position,
                                                                                         self.token.board.image),
                                                          pymunk.pygame_util.from_pygame(self.token.end_position,
                                                                                         self.token.board.image),
                                                          self.token.thickness,
                                                          )
            else:
                moment = pymunk_engine.moment_for_box(mass=mass,
                                                      size=(self.size[0] * self.token.width,
                                                            self.size[1] * self.token.height))
            # create body
            self.body = pymunk_engine.Body(mass=mass, moment=moment, body_type=body_type)
            if not self.gravity:
                self.body.velocity_func = lambda body, gravity, damping, dt: None


            # Sets the shape-type
            if self.shape_type.lower() == "rect":
                shape = pymunk.Poly.create_box(self.body,
                                               (self.size[0] * self.token.width,
                                                self.size[1] * self.token.height),
                                               )
            elif self.shape_type.lower() == "circle":
                shape = pymunk.Circle(self.body,
                                      self.size[0] * self.token.width / 2,
                                      (0, 0),
                                      )
            elif self.shape_type.lower() == "line":
                try:
                    start_x, start_y = self.token.start_position[0], self.token.start_position[1]
                    end_x, end_y = self.token.end_position[0], self.token.end_position[1]
                    shape = pymunk.Segment(self.body,
                                           pymunk.pygame_util.from_pygame((start_x, start_y),
                                                                          self.token.board.image),
                                           pymunk.pygame_util.from_pygame((end_x, end_y),
                                                                          self.token.board.image),
                                           self.token.thickness,
                                           )
                except AttributeError:
                    raise AttributeError("ERROR: token.board is not set.")
            # Adds object to space
            self.shape = shape
            PhysicsProperty.space.add(self.body, self.shape)
            if self.token.costume:
                self.body.position = pymunk.pygame_util.from_pygame(self.token.center,
                                                                    self.token.board.image)
            self.body.size = (self.token.width, self.token.height)
            #self.body.angle = math.radians(
            #        self.token.direction_at_unit_circle - self.token.costume.orientation )
            if self.shape_type.lower() != "line":
                PhysicsProperty.space.reindex_shapes_for_body(self.body)
            self.shape.friction = self.friction
            shape.elasticity = self.elasticity
            shape.token = self.token
            self.shape.collision_type = self.token.__class__.class_id
            self.dirty = 0
            self.model_setup_complete = True

    def reload_physics(self):
        if self.started:
            self.dirty = 1
            # Remove shape and body from space
            if self.body:
                for shape in list(self.body.shapes):
                    PhysicsProperty.space.remove(shape)
                PhysicsProperty.space.remove(self.body)
            # Set new properties and reset to space
            self.setup_physics_model()
            self.dirty = 0
            self.token.board._register_physics_collision_handler(self.token)

    def simulation_preprocess_token(self):
        """
        Updates the physics model in every frame

        Returns:

        """
        if not self.body.body_type == pymunk_engine.Body.STATIC:
            self.body.position = pymunk.pygame_util.from_pygame(self.token.position,self.token.board.image)
            PhysicsProperty.space.reindex_shapes_for_body(self.body)
            self.body.angle = math.radians(
                    self.token.direction_at_unit_circle + self.token.costume.orientation + self.correct_angle )

    @staticmethod
    def simulation(physics_tokens):
        [token.physics.simulation_preprocess_token() for token in physics_tokens if token.physics is not None]
        steps = PhysicsProperty.accuracy
        for x in range(steps):
            if PhysicsProperty.space is not None:
                PhysicsProperty.space.step(1 / (60 * steps))
        [token.physics.simulation_postprocess_token() for token in physics_tokens if token.physics is not None]

    def simulation_postprocess_token(self):
        """
        Reloads physics model from pygame data
        Returns:

        """
        if not self.body.body_type == pymunk_engine.Body.STATIC:
            self.token.position = pymunk.pygame_util.to_pygame(self.body.position, self.token.board.image)
            self.token.direction_at_unit_circle = math.degrees(self.body.angle) - self.token.costume.orientation - self.correct_angle
            self._velocity_x = self.body.velocity[0]
            self._velocity_y = self.body.velocity[1]
            if PhysicsProperty.debug:
                options = pymunk.pygame_util.DrawOptions(self.token.board.image)
                options.collision_point_color = (255, 20, 30, 40)
                PhysicsProperty.space.debug_draw(options)

    def remove(self):
        """
        Removes an object from physics-space
        """
        if self.body:
            PhysicsProperty.space.remove(self.body)
        if self.shape:
            PhysicsProperty.space.remove(self.shape)

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
        self._stable = value

    def impulse_in_direction(self, power):
        """
        Adds an impulse in token-direction

        Args:
            power: The power-value of the impulse.
        """
        impulse = pymunk.Vec2d(1, 0)
        impulse.rotate_degrees( self.token.direction_at_unit_circle - 270 )
        impulse = power * impulse.normalized()
        self.body.apply_impulse_at_local_point(impulse)
