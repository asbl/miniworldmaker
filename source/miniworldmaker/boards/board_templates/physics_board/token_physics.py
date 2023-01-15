import math
import sys
from typing import Optional
from typing import Union

import pymunk as pymunk_engine
import pymunk.pygame_util
from miniworldmaker.tokens import token as token
from miniworldmaker.tokens.token_plugins.shapes import shapes


class TokenPhysics:
    """Defines pyhsics-properties of a token, used as my_token.pyhsics.attribute or my_token.physics.method

    Can only be used for tokens on a PhysicsBoard.

    Examples:

        .. code-block:: python

            from miniworldmaker import *

            board = PhysicsBoard((800, 600))

            a = Circle()
            a.position = (75, 200)
            a.color = (255,0,0)
            a.physics.simulation = "simulated"
            a.direction = 180
            a.physics.shape_type = "circle"
            a.impulse(45, 1500)

            board.run()
    """

    def __init__(self, token, board):
        self.started: bool = False
        self._body_type = pymunk.Body.DYNAMIC
        self.board = board
        self.token: token.Token = token
        self.simulation: str = "simulated"
        self._gravity: bool = False
        self._stable: bool = False
        self._can_move: bool = True
        self._density: float = 10
        self.moment: Optional[float] = None
        self.damping = 1
        self.max_velocity_x = math.inf
        self._friction: float = 0.5
        self._velocity_x: float = 0
        self._velocity_y: float = 0
        self._elasticity: float = 0.5
        self._shape_type: str = "rect"
        self._correct_angle: float = 90
        self._body: Union[pymunk_engine.Body, None] = None
        self._shape: Union[pymunk_engine.Shape, None] = None
        self.dirty: int = 1
        self.has_physics: bool = False
        self._update_from_physics: bool = False  # is position/direction updated from physics_engine?
        self.size = (1, 1)  # scale factor for physics box model
        self.joints = []

    @staticmethod
    def velocity_function(body, gravity, damping, dt):
        pymunk.Body.update_velocity(body, gravity, body.physics_property.damping * damping, dt)
        if body.physics_property.max_velocity_x != math.inf and body.velocity[0] > body.physics_property.max_velocity_x:
            body.velocity = body.physics_property.max_velocity_x, body.velocity[1]
        if body.physics_property.max_velocity_x != math.inf and body.velocity[
            0] < - body.physics_property.max_velocity_x:
            body.velocity = - body.physics_property.max_velocity_x, body.velocity[1]

    def join(self, other: "token.Token"):
        """joins two tokens at their center points
        """
        if not hasattr(other, "physics"):
            raise TypeError("Other token has no attribute physics")
        my_body = self._body
        other_body = other.physics._body
        pj = pymunk.PinJoint(my_body, other_body, (0, 0), (0, 0))
        self.board.space.add(pj)
        return self.token.position_manager.get_position(), other.position

    def join(self, other: "token.Token", type="pin"):
        """joins two tokens at their center points
        """
        if not hasattr(other, "physics"):
            raise TypeError("Other token has no attribute physics")
        my_body = self._body
        other_body = other.physics._body
        pj = pymunk.PinJoint(my_body, other_body, (0, 0), (0, 0))
        self.joints.append(pj)
        self.board.space.add(pj)
        return self.token.position_manager.get_position(), other.position

    def remove_join(self, other: "token.Token"):
        """Remove a joint between two tokens.

        Removes a joint between two tokens, if a joint exists.

        Examples:

            Add and remove a joint on key_down:

            .. code-block:: python

                import random
                from miniworldmaker import *
                board = PhysicsBoard((400, 200))
                connected = False
                line = None
                anchor = Rectangle()
                anchor.size = (20,20)
                anchor.center = (100, 20)
                anchor.physics.simulation = "manual"
                other_side = Line((250,100),(500,200))
                def add_line(obj1, obj2):
                    l = Line(obj1.center, obj2.center)
                    l.physics.simulation = None
                    @l.register
                    def act(self):
                        self.start_position = obj1.center
                        self.end_position = obj2.center
                    return l
                c = Circle()
                @c.register
                def on_key_down(self, key):
                    global connected
                    global line
                    if not connected:
                        print("not connected")
                        self.physics.join(anchor)
                        line = add_line(self, anchor)
                        connected = True
                    else:
                        print("connected")
                        self.physics.remove_join(anchor)
                        line.remove()

                board.run()


            .. raw:: html

                <video loop autoplay muted width=400>
                <source src="../_static/jointsremove1.webm" type="video/webm">
                <source src="../_static/jointsremove1.mp4" type="video/mp4">
                Your browser does not support the video tag.
                </video>
        """
        for join in self.joints:
            if other.physics._body == join.b:
                self.board.space.remove(join)

    def _start(self):
        """Starts the physics-simulation

        Called in board-connector
        """
        if self.started == False:
            self.started = True
            self._setup_physics_model()  # After on_setup

    def _get_pymunk_shape(self):
        # Sets the shape-type_update_from_physics
        if self.shape_type.lower() == "rect":
            shape = pymunk.Poly.create_box(self._body,
                                           (self.size[0] * self.token.width,
                                            self.size[1] * self.token.height),
                                           1  # small radius
                                           )
        elif self.shape_type.lower() == "circle":
            shape = pymunk.Circle(self._body,
                                  self.size[0] * self.token.width / 2,
                                  (0, 0),
                                  )
        elif isinstance(self.token, shapes.Line):
            shift_x = 0
            shift_y = 0
            start = pymunk.pygame_util.from_pygame(
                (0, - self.token._length / 2),
                self.token.board.image)
            end = pymunk.pygame_util.from_pygame(
                (0, self.token._length / 2),
                self.token.board.image)
            shape = pymunk.Segment(self._body, start, end, self.token.thickness)
        else:
            raise AttributeError("No shape set!")
        return shape

    def _setup_physics_model(self):
        if self.dirty and self.token.position_manager.get_position():  # if token is on the board
            # create body
            self.has_physics = False
            self._body = pymunk_engine.Body(body_type=self.body_type)
            self._body.physics_property = self
            self._body.moment = math.inf
            self._body.velocity_func = self.velocity_function
            # self._body.damping = self.damping
            self._set_pymunk_position()
            self._set_pymunk_direction()
            self._body.size = (self.size[0] * self.token.width, self.size[1] * self.token.height)

            # disable velocity for tokens if token has no gravity
            if self.simulation == "static":
                self._body.velocity_func = lambda body, gravity, damping, dt: None
            else:
                self._body.velocity = self.velocity_x, self._velocity_y
            # Adds object to space
            if self._simulation != None:
                self._shape = self._get_pymunk_shape()
                self._shape.density = self.density
                self._shape.friction = self.friction
                self._shape.elasticity = self.elasticity
                self._shape.token = self.token
                self._shape.collision_type = hash(
                    self.token.__class__.__name__) % ((sys.maxsize + 1) * 2)
                self.board.space.add(self._body, self._shape)
            if self.moment is not None:
                self._body.moment = self.moment
            if self.simulation == "static":
                self.board.space.reindex_static()
            self.dirty = 1
            self.has_physics = True

    def _set_pymunk_position(self):
        pymunk_position = self.token.center[0], self.token.center[1]
        self._body.position = pymunk.pygame_util.from_pygame(
            pymunk_position, self.token.board.image)

    def _set_pymunk_direction(self):
        self._body.angle = self.token.position_manager.get_pymunk_direction_from_miniworldmaker()

    def _set_mwm_token_position(self):
        if self._body:
            self.token.center = pymunk.pygame_util.from_pygame(
                self._body.position, self.token.board.image)
            self.dirty = 0

    def _set_mwm_token_direction(self):
        self.token.position_manager.set_mwm_direction_from_pymunk()
        self.dirty = 0

    def reload(self):
        """Removes token from space and reloads physics_model
        """
        if self.started:
            self.dirty = 1
            # Remove shape and body from space
            self._remove_from_space()
            # Set new properties and reset to space
            self._setup_physics_model()
        else:
            self.dirty = 1

    def _remove_from_space(self):
        if self._body:
            for shape in list(self._body.shapes):
                if shape in self.board.space.shapes:
                    self.board.space.remove(shape)
            if self._body in self.board.space.bodies:
                self.board.space.remove(self._body)

    def remove(self):
        """Removes an object from physics-space
        """
        self._remove_from_space()

    @property
    def simulation(self):
        """Sets simulation type for token (`static`, `manual`, `simulated` or `None`)

        Sets simulation type for token:

        * `simulated`: Token is fully simulated by physics engine.
        * `manual`: Token is not affected by gravity.
        * `static`: Token is not moved by physics engine, but tokens can collide with token.
        * `None`: Token is not moved by physics engine and other tokens can't collige with token.
        """
        return self._simulation

    @simulation.setter
    def simulation(self, value: Union[str, None]):
        # Sets the simulation type
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
            self._is_rotatable = True
            self._gravity = True
            self._can_move = True
            self._stable = True
        self.dirty = 1
        self.reload()

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def body_type(self):
        """Returns body type of token

        Must not be used from outside - Use property simulation instead.
        """
        if self.simulation is None or self.simulation == "static":
            return pymunk.Body.STATIC
        elif self.simulation == "manual":
            return pymunk.Body.KINEMATIC
        else:
            return pymunk.Body.DYNAMIC

    @property
    def size(self):
        """Sets size of physics_object in relation to object

        * 1: Physics object size equals token size
        * < 1: Physics object is smaller than token
        * > 1: Physics object is larger than token.

        .. warning::

            Token is re-added to physics space after this operation - Velocity and impulses are lost.
        """
        return self._size

    @size.setter
    def size(self, value: tuple):
        self._size = value
        self.dirty = 1
        self.reload()

    @property
    def shape_type(self):
        """Sets shape type of object:

        Shape Types:
          * "rect": Rectangle
          * "circle": Circle

        (Planned for future relases: autogeometry)

        .. warning::

            Token is re-added to physics space after this operation - Velocity and impulses are lost.

        Examples:

            Demonstrate different shape types:

            .. code-block:: python

                from miniworldmaker import *

                board = PhysicsBoard(600,300)
                Line((0,100),(100,150))
                t = Token((0,50))
                t.physics.shape_type = "rect"
                Line((200,100),(300,150))
                t = Token((200,50))
                t.physics.shape_type = "circle"
                board.run()

            .. raw:: html

                <video loop autoplay muted width=400>
                <source src="../_static/shape_types.webm" type="video/webm">
                <source src="../_static/shape_types.mp4" type="video/mp4">
                Your browser does not support the video tag.
                </video>
        """
        return self._shape_type

    @shape_type.setter
    def shape_type(self, value: str):
        self._shape_type = value
        self.dirty = 1
        self.reload()

    @property
    def friction(self):
        """Sets friction of token

        .. warning::

            Token is re-added to physics space after this operation - Velocity and impulses are lost.

        """
        return self._friction

    @friction.setter
    def friction(self, value: float):
        self._friction = value
        self.dirty = 1
        self.reload()

    @property
    def elasticity(self):
        """Sets elasticity of token

        .. warning::

            Token is re-added to physics space after this operation - Velocity and impulses are lost.

        """
        return self._elasticity

    @elasticity.setter
    def elasticity(self, value: float):
        self._elasticity = value
        self.dirty = 1
        self.reload()

    @property
    def density(self):
        """Sets density of token

        .. warning::

            Token is re-added to physics space after this operation - Velocity and impulses are lost.

        """
        return self._density

    @density.setter
    def density(self, value: float):
        self._density = value
        self.dirty = 1
        self.reload()

    def _simulation_preprocess_token(self):
        """
        Updates the physics model in every frame

        Returns:

        """
        if (self._body and not self._body.body_type == pymunk_engine.Body.STATIC) and self.dirty:
            self._set_pymunk_position()
            self._set_pymunk_direction()
            self.board.space.reindex_shapes_for_body(self._body)
            self.dirty = 0

    def _set_update_mode(self):
        self._update_from_physics = True

    def _unset_update_mode(self):
        self._update_from_physics = False

    def _is_in_update_mode(self):
        return self._update_from_physics

    def _simulation_postprocess_token(self):
        """
        Reloads physics model from pygame data
        """
        if self.simulation and not math.isnan(self._body.position[0]):
            self._set_mwm_token_position()
            self._set_mwm_token_direction()
        if self._body and not self._body.body_type == pymunk_engine.Body.STATIC:
            self.velocity_x = self._body.velocity[0]
            self.velocity_y = self._body.velocity[1]
            if self.board.debug:
                options = pymunk.pygame_util.DrawOptions(self.token.board.image)
                options.collision_point_color = (255, 20, 30, 40)
                self.board.space.debug_draw(options)

    @property
    def velocity_x(self):
        """Sets velocity in x-direction. Can be positive or negative.

         Examples:

            Move a token left or right.

            .. code-block:: python

                def on_key_pressed_d(self):
                    self.physics.velocity_x = 50

                def on_key_pressed_a(self):
                    self.physics.velocity_x = - 50

        """
        return self._velocity_x

    @velocity_x.setter
    def velocity_x(self, value: float):
        self._velocity_x = value
        if self._body:
            self._body.velocity = value, self._body.velocity[1]

    @property
    def velocity_y(self):
        """Sets velocity in y-direction
        """
        return self._velocity_y

    @velocity_y.setter
    def velocity_y(self, value: float):
        self._velocity_y = value
        if self._body:
            self._body.velocity = self._body.velocity[0], value

    @property
    def is_rotatable(self):
        """defines, if token will be rotated by physics-engine.
        """
        return self._is_rotatable

    @is_rotatable.setter
    def is_rotatable(self, value: bool):
        self._is_rotatable = value
        self.dirty = 1
        self.reload()

    def force_in_direction(self, direction: float, power: float):
        force = pymunk.Vec2d(1, 0)
        force = force.rotated_degrees(
            360 - self.token.position_manager.dir_to_unit_circle(direction - self.token.direction))
        force = power * 1000 * force.normalized()
        self._body.apply_force_at_local_point(force)

    def impulse_in_direction(self, direction: float, power: float):
        """
        Adds an impulse in token-direction

        Examples:

            .. code-block:: python

                from miniworldmaker import *

                board = PhysicsBoard(300, 200)

                rect = Rectangle((280,120), 20, 80)
                rect.physics.simulation = "manual"
                ball = Circle((50,50),20)

                @rect.register
                def act(self):
                    rect.x -= 1
                    if rect.x == 0:
                        rect.x = 280

                @ball.register
                def on_key_down(self, key):
                    self.physics.impulse_in_direction(0, 5000)
                board.run()


        Args:
            power: The power-value of the impulse.
            direction: pymunk direction
        """
        impulse = pymunk.Vec2d(1, 0)
        impulse = impulse.rotated_degrees(
            360 - self.token.position_manager.dir_to_unit_circle(direction - self.token.direction))
        impulse = power * 1000 * impulse.normalized()
        self._body.apply_impulse_at_local_point(impulse)

    def force_in_direction(self, direction: float, power: float):
        """
        Adds a force in given direction

        Args:
            power: The power-value of the force.
            direction: pymunk direction
        """
        force = pymunk.Vec2d(1, 0)
        force = force.rotated_degrees(
            360 - self.token.position_manager.dir_to_unit_circle(direction - self.token.direction))
        force = power * 10000 * force.normalized()
        self._body.apply_force_at_local_point(force, (0, 0))
