import pymunk as pymunk_engine
import sys
import miniworldmaker.boards.board as board
import miniworldmaker.boards.token_connectors.physics_board_connector as physics_board_connector
import miniworldmaker.tools.token_inspection as token_inspection
import miniworldmaker.tools.token_class_inspection as token_class_inspection


class PhysicsBoard(board.Board):
    """
    A PhysicsBoard is a playing field on which objects follow physical laws.

    The PhysicsBoard itself defines some values with which the physics engine can be influenced, e.g.
    the gravity in the world.

    All tokens on a PhysicsBoard have an attribute ``token.physics``, with which you can change the physical properties
    of the object.
    """

    def __init__(
            self,
            columns: int = 40,
            rows: int = 40,
    ):
        super().__init__(columns, rows)
        self.gravity_x: float = 0
        self.gravity_y: float = 900
        self.debug: bool = False
        self._accuracy = 1
        self.space = pymunk_engine.Space()
        self.space.gravity = self.gravity_x, self.gravity_y
        self.space.iterations = 35
        self.space.damping = 0.9
        self.space.collision_persistence = 10
        self.physics_tokens = list()
        self.touching_methods = set()  # filled in token_manager
        self.separate_methods = set()  # filled in token_manager

    @property
    def accuracy(self):
        """Sets number of physics-steps performed in each frame.

        Default: 1
        """
        return self._accuracy

    @accuracy.setter
    def accuracy(self, value: int):
        self._accuracy = value

    def _pymunk_register_collision_manager(self, token, other_class, event, method):
        """Adds pymunk collision handler, which is evaluated by pymunk engine.

        The event (begin, end) and the method (on_touching...) are added as data to the handler

        Args:
            token: The token
            other_class: The class which should be detected by collision handler
            event: The pymunk-event  (begin or separate)
            method: The method, e.g. on_touching_token or on_separation_from_token. Last part is a class name

        :meta private:
        """

        space = self.space
        token_id = hash(token.__class__.__name__) % ((sys.maxsize + 1) * 2)
        other_id = hash(other_class.__name__) % ((sys.maxsize + 1) * 2)
        handler = space.add_collision_handler(token_id, other_id)
        handler.data["method"] = getattr(token, method.__name__)
        handler.data["type"] = event
        if event == "begin":
            handler.begin = self.pymunk_touching_collision_listener
        if event == "separate":
            handler.separate = self.pymunk_separation_collision_listener

    def get_token_connector(self, token):
        """Gets connector to PhysicsBoard

        :meta private:
        """
        return physics_board_connector.PhysicsBoardConnector(self, token)

    def get_physics_collision_methods_for_token(self, token):
        """Gets all collision methods for token

        :meta private:
        """
        return [
            getattr(token, method_name)
            for method_name in dir(token)
            if hasattr(token, method_name)
               and callable(getattr(token, method_name))
               and method_name.startswith("on_touching_")
               or method_name.startswith("on_separation_from_")
        ]

    def register_all_physics_collision_managers_for_token(self, token):
        """Registers on__touching and on_seperation-Methods to token.
        If new_class is set, only methods with new class (e.g. on_touching_new_class are set)

        :meta private:
        """
        collision_methods = self.get_physics_collision_methods_for_token(token)
        for method in collision_methods:
            if method.__name__.startswith("on_touching_"):
                self.register_touching_method(method)
            elif method.__name__.startswith("on_separation_from_"):
                self.register_separate_method(method)

    def _register_physics_listener_method(self, method, event, other_cls):
        """Registers a physics listener method. (on touching or on_seperation.)
        Called from register_touching_method and register_separate_method

        :meta private:
        """
        token_class_inspect = token_class_inspection.TokenClassInspection(self)
        all_token_classes = token_class_inspect.get_all_token_classes()
        if other_cls not in all_token_classes:
            return False
        else:
            subclasses_of_other_token = token_class_inspection.TokenClassInspection(other_cls).get_subclasses_for_cls()
            for other_subcls in subclasses_of_other_token:
                # If you register a Collision with a Token, collissns with subclasses of the token
                # are also registered
                self._pymunk_register_collision_manager(method.__self__, other_subcls, event, method)
                return True

    def register_touching_method(self, method):
        """
        Registers on_touching_[class] method

        :meta private:
        """
        event = "begin"
        other_cls_name = method.__name__[len("on_touching_"):].lower()
        other_cls = token_class_inspection.TokenClassInspection(self).find_token_class_by_classname(other_cls_name)
        if self._register_physics_listener_method(method, event, other_cls):
            self.touching_methods.add(method)

    def register_separate_method(self, method):
        """
        Registers on_separation_from_[class] method

        :meta private:
        """
        event = "separate"
        other_cls_name = method.__name__[len("on_separation_from_"):].lower()
        other_cls = token_class_inspection.TokenClassInspection(self).find_token_class_by_classname(other_cls_name)
        if self._register_physics_listener_method(method, event, other_cls):
            self.separate_methods.add(method)

    def remove_token_from_board(self, token):
        """Removes token from board and removes pymunk body and shapes.
        """
        super().remove_token_from_board(token)
        self.physics_tokens.remove(token)

    def act_all(self):
        """Handles acting of tokens - Calls the physics-simulation in each frame.

        :meta private:
        """
        super().act_all()
        self.simulate_all_physics_tokens()

    def simulate_all_physics_tokens(self):
        """Iterates over all tokens and process physics-simulation

        Processes phyisics-simulation in three steps

        * Convert miniworldmaker-position/direction to pymunk position/direction
        * Simulate a step in physics-engine
        * Convert pymunk position/direction to miniworldmaker position/direction

        :meta private:
        """
        if len(self.physics_tokens) > 0:
            # pre-process
            [token.physics._set_update_mode() for token in self.physics_tokens]
            [token.physics._simulation_preprocess_token() for token in self.physics_tokens]
            # simulate
            steps = self.accuracy
            for _ in range(steps):
                # if self.physics.space is not None: - can be removed
                self.space.step(1 / (60 * steps))
            # post-process
            [token.physics._simulation_postprocess_token() for token in self.physics_tokens]
            [token.physics._unset_update_mode() for token in self.physics_tokens]

    @property
    def gravity(self):
        """ Defines gravity in physics board.
        Default gravity: x=0, y=500
        :return:
        """
        return self.gravity_x, self.gravity_y

    @gravity.setter
    def gravity(self, value: tuple):
        self.gravity_x = value[0]
        self.gravity_y = value[1]
        self.space.gravity = self.gravity_x, self.gravity_y

    @property
    def damping(self):
        """ Amount of simple damping to apply to the space.

        A value of 0.9 means that each body will lose 10% of its velocity per second. Defaults to 1.
        """
        return self.gravity_x, self.gravity_y

    @damping.setter
    def damping(self, value: tuple):
        self._damping = value
        self.space.damping = self._damping

    def pymunk_touching_collision_listener(self, arbiter, space, data):
        """Handles collisions - Handled by pymunk engine

        :meta private:
        """
        # Translate pymunk variables to miniworldmaker variables
        token = arbiter.shapes[0].token
        other = arbiter.shapes[1].token
        collision = dict()
        # get touching token_manager for token
        for method in self.touching_methods:
            method_other_cls_name = method.__name__[len("on_touching_"):].lower()
            method_other_cls = token_class_inspection.TokenClassInspection(self).find_token_class_by_classname(
                method_other_cls_name
            )
            # is other an instance of method_other_cls
            if isinstance(other, method_other_cls):
                token_inspection.TokenInspection(token).get_and_call_method(method.__name__, [other, collision])
        return True

    def pymunk_separation_collision_listener(self, arbiter, space, data):
        """Handles collisions - Handled by pymunk engine

        :meta private:
        """
        # Translate pymunk variables to miniworldmaker variables
        token = arbiter.shapes[0].token
        other = arbiter.shapes[1].token
        collision = dict()
        # get separation token_manager for token
        for method in self.separate_methods:
            method_other_cls_name = method.__name__[len("on_separation_from_"):].lower()
            method_other_cls = token_class_inspection.TokenClassInspection(self).find_token_class_by_classname(
                method_other_cls_name
            )
            # is other an instance of method_other_cls
            if isinstance(other, method_other_cls):
                token_inspection.TokenInspection(token).get_and_call_method(method.__name__, [other, collision])
        return True
