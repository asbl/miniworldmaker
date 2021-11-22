import pymunk as pymunk_engine
from miniworldmaker.boards import pixel_board  as pixel_board_module
from miniworldmaker.tools import inspection_methods as im
from miniworldmaker.boards.token_connectors.physics_board_connector import PhysicsBoardConnector

class PhysicsBoard(pixel_board_module.PixelBoard):

    def __init__(self,
                 columns: int = 40,
                 rows: int = 40,
                 tile_size : int = 1,
                 tile_margin : int = 0,
                 background_image=None
                 ):
            self.gravity_x = 0
            self.gravity_y = -900
            self.debug = False
            self.collision_types = list
            self.accuracy = 1
            self.space = pymunk_engine.Space()
            self.space.gravity = self.gravity_x, self.gravity_y
            self.space.iterations = 35
            self.space.damping = 0.9
            self.space.collision_persistence = 10
            self.physics_tokens = list()
            self.touching_methods = list()  # filled in token_handler
            self.separation_methods = list()  # filled in token_handler
            # Note: This is the grandparent constructor
            super(pixel_board_module.PixelBoard, self).__init__(columns, rows, tile_size, tile_margin, background_image)

    def get_token_connector(self, token):
        return PhysicsBoardConnector(self, token)

    @staticmethod
    def get_touching_method_other_class(method):
        other_cls_name = method.__name__[len("on_touching_"):].lower()
        other_cls = im.InspectionMethods.get_token_class_by_name(other_cls_name)
        return other_cls

    @staticmethod
    def get_separation_method_other_class(method):
        other_cls_name = method.__name__[len("on_separation_from_"):].lower()
        other_cls = im.InspectionMethods.get_token_class_by_name(other_cls_name)
        return other_cls

    def get_physics_handlers(self, token):
        methods = [getattr(token, method_name) for method_name in dir(token)
                   if hasattr(token, method_name) and callable(getattr(token, method_name))
                   and method_name.startswith("on_touching_") or method_name.startswith("on_separation_from_")]
        return methods

    def register_all_physics_handlers(self, token):
        physics_handlers = self.get_physics_handlers(token)
        for method in physics_handlers:
            self.register_physics_handlers(token, method)

    def register_physics_handlers(self, token, method):
        if method.__name__.startswith("on_touching_") or method.__name__.startswith("on_separation_from_"):
            if method.__name__.startswith("on_touching_"):
                event = "begin"
                other_cls = PhysicsBoard.get_touching_method_other_class(method)
                self.touching_methods.append(method)
            elif method.__name__.startswith("on_separation_from_"):
                event = "separate"
                other_cls = PhysicsBoard.get_separation_method_other_class(method)
                self.separate_methods.append(method)
            child_classes = other_cls.all_subclasses()
            for child_class in child_classes:
                # Add physics handler for class and all subclasses
                self._pymunk_register_collision_handler(token, child_class, event, method)
            self._pymunk_register_collision_handler(token, other_cls, event, method)

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
            method_other_cls = im.InspectionMethods.get_token_class_by_name(method_other_cls_name)
            # is other an instance of method_other_cls
            if isinstance(other, method_other_cls):
                im.InspectionMethods.get_and_call_instance_method(
                    token, method.__name__, [self, collision])
            # Korrekte Methode ist da
            #handler_cls = PhysicsBoard.get_touching_method_other_class(method)
        return True

    def pymunk_separation_collision_listener(self, arbiter, space, data):
        # Translate pymunk variables to miniworldmaker variables
        collision_method_for_token = None
        token = arbiter.shapes[0].token
        other = arbiter.shapes[1].token
        collision = dict()
        # get separation token_handler for token
        for method in self.separation_methods:
            method_other_cls_name = method.__name__[len("on_separation_from_"):].lower()
            method_other_cls = im.InspectionMethods.get_token_class_by_name(method_other_cls_name)
            # is other an instance of method_other_cls
            if isinstance(other, method_other_cls):
                im.InspectionMethods.get_and_call_instance_method(
                    token, method.__name__, [self, collision])
            # Korrekte Methode ist da
            #handler_cls = PhysicsBoard.get_touching_method_other_class(method)
        return True
