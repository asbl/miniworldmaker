import pymunk as pymunk_engine
import pymunk.pygame_util
import sys
from typing import Union


class TokenPhysics:

    """
    The PhysicsProperty class describes all properties necessary to physically
    simulate an object using the pymunk engine.

    The properties are defined in the method setup_physics().
    You can override this method if you want your class to have different physical properties.

    For an object to be physically simulated,
    the method start_physics() must first be called.

    Examples:
        >>> class Player(Token):
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
        is_rotatable: If True, the Object has no moment and can't be rotated by an impulse
        can_move: Defines if the object can move
        gravity: Defines if the object affected by gravity
        shape_type: line, circle or rect
    """

    def __init__(self, token, board):
        self.started: bool = False
        self._body_type = pymunk.Body.DYNAMIC
        self.board = board
        self.token: token.Token = token
        self.simulation: str = "simulated"
        self._mass: float = 1
        self._gravity: bool = False
        self._stable: bool = False
        self._can_move: bool = True
        self.density: float = 10
        self._friction: float = 10
        self._velocity_x: float = 0
        self._velocity_y: float = 0
        self._elasticity: float = 0.5
        self._shape_type: str = "rect"
        self._correct_angle: float = 90
        self._body: Union[pymunk_engine.Body, None] = None
        self._shape: Union[pymunk_engine.Shape, None] = None
        self.dirty: int = 1
        self.model_setup_complete: bool = False
        self.size = (1, 1)  # scale factor for physics box model

    def start(self):
        """
        Starts the physcis-simulation for this object. If you want to use Physics-Sumulation with your object,
        you have to use this method.

        WARNING: This method should be called AFTER all changes of attributes but BEFORE you add an impulse to the object
        If you implement a setup_physics()-Method in an token, you don't have to call this method.

        Examples:
            >>> # These attributes are changed BEFORE start_physics()
            >>> self.physics.size = 0.7, 0.7
            >>> self.physics.shape_type = "circle"
            >>> self.physics.is_rotatable = False
            >>> # The physics simulation is started
            >>> self.start_physics()
            >>> # The impulse is applied to the object AFTER starting the physics simulation
            >>> self.physics.velocity_x = 1500
            >>> self.physics.velocity_y = - self.board.arrow.direction * 50
        """
        if self.started == False:
            self.started = True
            # self.count_tokens += 1
            self.setup_physics_model()  # After on_setup

    def get_pymunk_shape(self):
        # Sets the shape-type
        if self.shape_type.lower() == "rect":
            shape = pymunk.Poly.create_box(self._body,
                                           (self.size[0] * self.token.width,
                                            self.size[1] * self.token.height),
                                           2  # small radius
                                           )
        elif self.shape_type.lower() == "circle":
            shape = pymunk.Circle(self._body,
                                  self.size[0] * self.token.width / 2,
                                  (0, 0),
                                  )
        elif self.shape_type.lower() == "line":
                # pymunk 5.6 values
                #shift_x = self.token.size[0] / 2 + self.token.position[0]
                #shift_y = - (self.token.board.size[1] - self.token.size[1] / 2 - self.token.position[1])
                shift_x = self.token.size[0] / 2 + self.token.position[0]
                shift_y = self.token.size[1] / 2 + self.token.position[1]
                start = pymunk.pygame_util.from_pygame(
                    (self.token.start_position[0] - shift_x, self.token.start_position[1] - shift_y), self.token.board.image)
                end = pymunk.pygame_util.from_pygame(
                    (self.token.end_position[0] - shift_x, self.token.end_position[1] - shift_y), self.token.board.image)
                shape = pymunk.Segment(self._body, start, end, self.token.thickness)
        else:
            raise AttributeError("No shape set!")
        return shape

    def setup_physics_model(self):
        if self.dirty and self.token.position:  # if token is on board
            # create body
            self._body = pymunk_engine.Body(body_type=self.body_type)
            self.set_pymunk_position()
            self.set_pymunk_direction()
            self._body.size = (self.size[0] * self.token.width, self.size[1] * self.token.height)
            # disable velocity for tokens if token has no gravity
            if self.simulation == "static":
                self._body.velocity_func = lambda body, gravity, damping, dt: None
            else:
                self._body.velocity = self.velocity_x, self._velocity_y
            # Adds object to space
            if self._simulation != None:
                self._shape = self.get_pymunk_shape()
                self._shape.density = self.density
                self._shape.friction = self.friction
                self._shape.elasticity = self.elasticity
                self._shape.token = self.token
                self._shape.collision_type = hash(
                    self.token.__class__.__name__) % ((sys.maxsize + 1) * 2)
                self.board.space.add(self._body, self._shape)
            if self.simulation == "static":
                self.board.space.reindex_static()
            self.dirty = 1
            self.model_setup_complete = True

    def set_pymunk_position(self):
        pymunk_position = self.token.center[0], self.token.center[1]
        self._body.position = pymunk.pygame_util.from_pygame(
            pymunk_position, self.token.board.image)

    def set_pymunk_direction(self):
        self._body.angle = self.token.position_manager.get_pymunk_direction_from_miniworldmaker()

    def set_mwm_token_position(self):
        self.token.center = pymunk.pygame_util.from_pygame(
            self._body.position, self.token.board.image)
        self.dirty = 0

    def set_mwm_token_direction(self):
        self.token.position_manager.set_mwm_direction_from_pymunk()
        self.dirty = 0

    def reload(self):
        if self.started:
            self.dirty = 1
            # Remove shape and body from space
            if self._body:
                for shape in list(self._body.shapes):
                    self.board.space.remove(shape)
                self.board.space.remove(self._body)
            # Set new properties and reset to space
            self.setup_physics_model()
        else:
            self.dirty = 1

    @property
    def simulation(self):
        return self._simulation

    @simulation.setter
    def simulation(self, value: str):
        # Sets the body type:
        # dynamic: Influenced by physic (e.g. actors)
        # static: not influenced by physics (e.g. plattforms)
        # kinematic: e.g. moving plattforms
        self._simulation = value
        if value == None:
            self._is_rotatable = False
            self._gravity = False
            self._can_move = False
            self._stable = True
        elif value.lower() == "static":
            self._is_rotatable = False
            self._gravity = False
            self._can_move = False
            self._stable = True
            self.density = 0
        elif value.lower() == "manual":
            self._is_rotatable = True
            self._gravity = False
            self._can_move = True
            self._stable = True
        elif value.lower() == "simulated":
            self._is_rotatable = False
            self._gravity = True
            self._can_move = True
            self._stable = False
        self.dirty = 1
        self.reload()

    @property
    def body_type(self):
        if self.simulation is None or self.simulation == "static":
            return pymunk.Body.STATIC
        elif self.simulation == "manual":
            return pymunk.Body.KINEMATIC
        else:
            return pymunk.Body.DYNAMIC

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value: tuple):
        self._size = value
        self.dirty = 1
        self.reload()

    @property
    def shape_type(self):
        return self._shape_type

    @shape_type.setter
    def shape_type(self, value: str):
        self._shape_type = value
        self.dirty = 1
        self.reload()

    @property
    def friction(self):
        return self._friction

    @friction.setter
    def friction(self, value: float):
        self._friction = value
        self.dirty = 1
        self.reload()

    @property
    def elasticity(self):
        return self._elasticity

    @elasticity.setter
    def elasticity(self, value: float):
        self._elasticity = value
        self.dirty = 1
        self.reload()

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value: Union[float, str]):
        # mass
        if value != "inf":
            self._mass = value
        else:
            self._mass = float("inf")
        self.dirty = 1
        self.reload()

    def simulation_preprocess_token(self):
        """
        Updates the physics model in every frame

        Returns:

        """
        if (self._body and not self._body.body_type == pymunk_engine.Body.STATIC) and self.dirty:
            self.set_pymunk_position()
            self.set_pymunk_direction()
            self.board.space.reindex_shapes_for_body(self._body)
            self.dirty = 0

    def simulation_postprocess_token(self):
        """
        Reloads physics model from pygame data
        Returns:

        """
        self.set_mwm_token_position()
        self.set_mwm_token_direction()
        if self._body and not self._body.body_type == pymunk_engine.Body.STATIC:
            self.velocity_x = self._body.velocity[0]
            self.velocity_y = self._body.velocity[1]
            if self.board.debug:
                options = pymunk.pygame_util.DrawOptions(self.token.board.image)
                options.collision_point_color = (255, 20, 30, 40)
                self.board.space.debug_draw(options)

    def remove(self):
        """
        Removes an object from physics-space
        """
        if self._body:
            for shape in list(self._body.shapes):
                self.board.space.remove(shape)
            self.board.space.remove(self._body)

    @property
    def velocity_x(self):
        return self._velocity_x

    @velocity_x.setter
    def velocity_x(self, value: float):
        self._velocity_x = value
        if self._body:
            self._body.velocity = value, self._body.velocity[1]

    @property
    def velocity_y(self):
        return self._velocity_y

    @velocity_y.setter
    def velocity_y(self, value: float):
        self._velocity_y = value
        if self._body:
            self._body.velocity = self._body.velocity[0], value

    @property
    def is_rotatable(self):
        return self._is_rotatable

    @is_rotatable.setter
    def is_rotatable(self, value: bool):
        self._is_rotatable = value

    def impulse_in_direction(self, direction: float, power: float):
        """
        Adds an impulse in token-direction

        Args:
            power: The power-value of the impulse.
            direction: pymunk direction
        """
        impulse = pymunk.Vec2d(1, 0)
        impulse = impulse.rotated_degrees(direction)
        impulse = power * 1000 * impulse.normalized()
        self._body.apply_impulse_at_local_point(impulse)

    def force_in_direction(self, direction: float, power: float):
        """
        Adds an force in token-direction

        Args:
            power: The power-value of the force.
            direction: pymunk direction
        """
        force = pymunk.Vec2d(1, 0)
        force = force.rotated_degrees(direction)
        force = power * 10000 * force.normalized()
        self._body.apply_force_at_local_point(force, (0, 0))
