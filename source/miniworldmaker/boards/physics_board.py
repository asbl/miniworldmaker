import pymunk as pymunk_engine
import sys
from miniworldmaker.boards import pixel_board as pixel_board_module
from miniworldmaker.boards.token_connectors.physics_board_connector import PhysicsBoardConnector
from miniworldmaker.tools import token_inspection
from miniworldmaker.tools import token_class_inspection
import miniworldmaker

class PhysicsBoard(miniworldmaker.PixelBoard):

    def __init__(self,
                 columns: int = 40,
                 rows: int = 40,
                 tile_size: int = 1,
                 tile_margin: int = 0,
                 background_image=None
                 ):
        super(pixel_board_module.PixelBoard, self).__init__(
            columns, rows, tile_size, tile_margin, background_image)
        self.gravity_x: float = 0
        self.gravity_y: float = 900
        self.debug: bool = False
        self.accuracy = 1
        self.space = pymunk_engine.Space()
        self.space.gravity = self.gravity_x, self.gravity_y
        self.space.iterations = 35
        self.space.damping = 0.9
        self.space.collision_persistence = 10
        self.physics_tokens = list()
        self.touching_methods = set()  # filled in token_handler
        self.separate_methods = set()  # filled in token_handler

    def _pymunk_register_collision_handler(self, token, other_class, event, method):
        """
        Adds pymunk collission handler, which is evaluated by pymunk engine.
        The event (begin, end) and the method (on_touching...) are added as data to the handler

        Args:
            token: The token
            other_class: The class which should be detected by collision handler
            event: The pymunk-event  (begin or separate)
            method: The method, e.g. on_touching_token or on_separation_from_token. Last part is a class name       
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
        return PhysicsBoardConnector(self, token)

    def get_physics_collision_methods_for_token(self, token):
        return [getattr(token, method_name) for method_name in dir(token)
                if hasattr(token, method_name) and callable(getattr(token, method_name))
                and method_name.startswith("on_touching_") or method_name.startswith("on_separation_from_")]

    def register_all_physics_collision_handlers_for_token(self, token):
        """
        Registers on__touching and on_seperation-Methods to token.
        If new_class is set, only methods with new class (e.g. on_touching_new_class are se.t)
        """
        collision_methods = self.get_physics_collision_methods_for_token(token)
        for method in collision_methods:
            if method.__name__.startswith("on_touching_"):
                self.register_touching_method(method)
            elif method.__name__.startswith("on_separation_from_"):
                self.register_separate_method(method)

    def _register_physics_listener_method(self, method, event, other_cls):
        """"
        Registers a physics listener method. (on touching or on_seperation.)
        Called from register_touching_method and register_separate_method
        """
        token_class_inspect = token_class_inspection.TokenClassInspection(self)
        all_token_classes = token_class_inspect.get_all_token_classes()
        print("i will register...", method, other_cls, all_token_classes)
        if other_cls not in all_token_classes:
            return False
        else:
            subclasses_of_other_token = token_class_inspection.TokenClassInspection(
                other_cls).get_subclasses_for_cls()
            for other_subcls in subclasses_of_other_token:
                # If you register a Collission with a Token, collissions with subclasses of the token
                # are also registered
                self._pymunk_register_collision_handler(
                    method.__self__, other_subcls, event, method)
                print("Registered...", method)
                return True

    def register_touching_method(self, method):
        event = "begin"
        other_cls_name = method.__name__[len("on_touching_"):].lower()
        other_cls = token_class_inspection.TokenClassInspection(
            self).find_token_class_by_classname(other_cls_name)
        if self._register_physics_listener_method(method, event, other_cls):
            self.touching_methods.add(method)

    def register_separate_method(self, method):
        event = "separate"
        other_cls_name = method.__name__[len("on_separation_from_"):].lower()
        other_cls = token_class_inspection.TokenClassInspection(
            self).find_token_class_by_classname(other_cls_name)
        if self._register_physics_listener_method(method, event, other_cls):
            self.separate_methods.add(method)

    def remove_token_from_board(self, token):
        super().remove_token_from_board(token)
        self.physics_tokens.remove(token)

    def act_all(self):
        super().act_all()
        self.simulate_all_physics_tokens()

    def simulate_all_physics_tokens(self):
        if len(self.physics_tokens) > 0:
            # preprocess
            [token.physics.simulation_preprocess_token()
             for token in self.physics_tokens]
            # simulate
            steps = self.accuracy
            for _ in range(steps):
                # if self.physics.space is not None: - can be removed
                self.space.step(1 / (60 * steps))
            # postprocess
            [token.physics.simulation_postprocess_token()
             for token in self.physics_tokens]

    @property
    def gravity(self):
        return self.gravity_x, self.gravity_y

    @gravity.setter
    def gravity(self, value: tuple):
        self.gravity_x = value[0]
        self.gravity_y = value[1]
        self.space.gravity = self.gravity_x, self.gravity_y

    @property
    def damping(self):
        return self.gravity_x, self.gravity_y

    @damping.setter
    def damping(self, value: tuple):
        self._damping = value
        self.space.damping = self._damping

    def pymunk_touching_collision_listener(self, arbiter, space, data):
        """
        This is called by pymunk engine if there is a collision
        """
        # Translate pymunk variables to miniworldmaker variables
        token = arbiter.shapes[0].token
        other = arbiter.shapes[1].token
        collision = dict()
        # get touching token_handler for token
        for method in self.touching_methods:
            method_other_cls_name = method.__name__[len("on_touching_"):].lower()
            method_other_cls = token_class_inspection.TokenClassInspection(
                self).find_token_class_by_classname(method_other_cls_name)
            # is other an instance of method_other_cls
            if isinstance(other, method_other_cls):
                token_inspection.TokenInspection(token).get_and_call_method(
                    method.__name__, [other, collision])
        return True

    def pymunk_separation_collision_listener(self, arbiter, space, data):
        # Translate pymunk variables to miniworldmaker variables
        token = arbiter.shapes[0].token
        other = arbiter.shapes[1].token
        collision = dict()
        # get separation token_handler for token
        for method in self.separate_methods:
            method_other_cls_name = method.__name__[len("on_separation_from_"):].lower()
            method_other_cls = token_class_inspection.TokenClassInspection(
                self).find_token_class_by_classname(method_other_cls_name)
            # is other an instance of method_other_cls
            if isinstance(other, method_other_cls):
                token_inspection.TokenInspection(token).get_and_call_method(
                    method.__name__, [other, collision])
        return True
