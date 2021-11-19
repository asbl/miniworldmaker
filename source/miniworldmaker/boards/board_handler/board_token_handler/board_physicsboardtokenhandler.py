import miniworldmaker.tokens.sensors.token_pixelboardsensor as pixelboardsensor
import miniworldmaker.tokens.costumes.token_physics_costume_manager as physicsboardcostumemanager
import miniworldmaker.tokens.positions.token_physics_position_manager as physicspositionmanager
import miniworldmaker.boards.board_handler.board_token_handler.board_pixelboardtokenhandler as pixelboardtokenhandler
from miniworldmaker.board_positions import board_position
from miniworldmaker.tokens import token_physics
from miniworldmaker import inspection_methods as im
import sys


class PhysicsBoardTokenHandler(pixelboardtokenhandler.PixelBoardTokenHandler):

    count_tokens = 0

    def __init__(self, board):
        super().__init__(board)
        self.touching_methods = list()  # filled in token_handler
        self.separation_methods = list()  # filled in token_handler
        self.physics_tokens = list()

    def add_position_manager_to_token(self, token, position):
        token.position_manager = physicspositionmanager.PhysicsBoardPositionManager(token, position)
        token._managers.append(token.position_manager)

    def add_token_to_board(self, token, position: board_position.BoardPosition):
        super().add_token_to_board(token, position)
        self.register_all_physics_handlers(token)

    def add_board_costume_manager_to_token(self, token, image):
        token.costume_manager = physicsboardcostumemanager.PhysicsBoardCostumeManager(token, image)
        token._managers.append(token.costume_manager)

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
            steps = self.board.accuracy
            for _ in range(steps):
                # if self.physics.space is not None: - can be removed
                self.board.space.step(1 / (60 * steps))
            # postprocess
            [token.physics.simulation_postprocess_token()
             for token in self.physics_tokens]

    def register_token_method(self, token, method: callable):
        """
        Bind a touching method to pymunk engine, e.g.: 
        if method on_touching_token
        is registered, in pymunk are following handlers registered:
        handler for (self.__class__, Token.__class_)
        handler for (self.__class__, player.class.__class__)
        handler for (self.__class__, wall.class.__class__)
        (because Player and Wall are subclasses of Token)
        """
        super().register_token_method(token, method)
        # Register physic collision methods
        self.register_physics_handlers(token, method)

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
                other_cls = PhysicsBoardTokenHandler.get_touching_method_other_class(method)
                self.touching_methods.append(method)
            elif method.__name__.startswith("on_separation_from_"):
                event = "separate"
                other_cls = PhysicsBoardTokenHandler.get_separation_method_other_class(method)
                self.separate_methods.append(method)
            child_classes = other_cls.all_subclasses()
            for child_class in child_classes:
                # Add physics handler for class and all subclasses
                self._pymunk_register_collision_handler(token, child_class, event, method)
            self._pymunk_register_collision_handler(token, other_cls, event, method)

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

        space = self.board.space
        token_id = hash(token.__class__.__name__) % ((sys.maxsize + 1) * 2)
        other_id = hash(other_class.__name__) % ((sys.maxsize + 1) * 2)
        handler = space.add_collision_handler(token_id, other_id)
        handler.data["method"] = getattr(token, method.__name__)
        handler.data["type"] = event
        if event == "begin":
            handler.begin = self.pymunk_touching_collision_listener
        if event == "separate":
            handler.separate = self.pymunk_separation_collision_listener

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
                    token, method.__name__, [other, collision])
            # Korrekte Methode ist da
            PhysicsBoardTokenHandler.get_touching_method_other_class(method)
        return True

    def pymunk_separation_collision_listener(self, arbiter, space, data):
        # Translate pymunk variables to miniworldmaker variables
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
                    token, method.__name__, [other, collision])
            # Korrekte Methode ist da
            PhysicsBoardTokenHandler.get_touching_method_other_class(method)
        return True
