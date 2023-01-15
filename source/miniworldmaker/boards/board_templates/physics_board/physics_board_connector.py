import miniworldmaker.boards.board_templates.pixel_board.pixel_board_connector as pixelboard_connector
import miniworldmaker.boards.board_templates.physics_board.token_physics as token_physics
import miniworldmaker.boards.board_templates.physics_board.token_physics_position_manager as physicspositionmanager
import miniworldmaker.boards.board_templates.pixel_board.token_pixelboardsensor as token_pixelboardsensor
import miniworldmaker.tools.token_class_inspection as token_class_inspection
import miniworldmaker.boards.board_templates.physics_board.physics_board as board_mod
import miniworldmaker.tokens.token as token_mod
import sys


class PhysicsBoardConnector(pixelboard_connector.PixelBoardConnector):
    count_tokens = 0

    def __init__(self, board: "board_mod.PhysicsBoard", token: "token_mod.Token"):
        super().__init__(board, token)
        self.board: "board_mod.PhysicsBoard" = board

    @staticmethod
    def get_position_manager_class():
        return physicspositionmanager.PhysicsBoardPositionManager

    @staticmethod
    def get_board_sensor_class():
        return token_pixelboardsensor.TokenPixelBoardSensor

    def add_token_to_board(self):
        # add token.physics attribute with physics properties to token
        self.token.physics = token_physics.TokenPhysics(self.token, self.token.board)
        if hasattr(self.token, "set_physics_default_values"):
            self.token.set_physics_default_values()
        super().add_token_to_board()
        self.register_all_physics_collision_managers_for_token()
        self.token.physics._start()
        self.board.physics_tokens.append(self.token)
        if hasattr(self.token, "on_begin_simulation"):
            self.token.on_begin_simulation()

    def remove_token_from_board(self):
        super().remove_token_from_board()
        self.board.physics_tokens.remove(self.token)

    def register_all_physics_collision_managers_for_token(self):
        """Registers on__touching and on_separation-Methods to token.
        If new_class is set, only methods with new class (e.g. on_touching_new_class are set)

        :meta private:
        """
        collision_methods = self.board.get_physics_collision_methods_for_token(self.token)
        for method in collision_methods:
            if method.__name__.startswith("on_touching_"):
                self.register_touching_method(method)
            elif method.__name__.startswith("on_separation_from_"):
                self.register_separate_method(method)

    def register_touching_method(self, method):
        """
        Registers on_touching_[class] method

        :meta private:
        """
        event = "begin"
        other_cls_name = method.__name__[len("on_touching_"):].lower()
        other_cls = token_class_inspection.TokenClassInspection(self).find_token_class_by_classname(other_cls_name)
        if self._register_physics_listener_method(method, event, other_cls):
            self.board.touching_methods.add(method)

    def register_separate_method(self, method):
        """
        Registers on_separation_from_[class] method

        :meta private:
        """
        event = "separate"
        other_cls_name = method.__name__[len("on_separation_from_"):].lower()
        other_cls = token_class_inspection.TokenClassInspection(self).find_token_class_by_classname(other_cls_name)
        if self._register_physics_listener_method(method, event, other_cls):
            self.board.separate_methods.add(method)

    def _register_physics_listener_method(self, method, event, other_cls):
        """Registers a physics listener method. (on touching or on_separation.)
        Called from register_touching_method and register_separate_method

        :meta private:
        """
        token_class_inspect = token_class_inspection.TokenClassInspection(self)
        all_token_classes = token_class_inspect.get_all_token_classes()
        if other_cls not in all_token_classes:
            return False
        else:
            subclasses_of_other_token = token_class_inspection.TokenClassInspection(other_cls).get_subclasses_for_cls()
            for other_subcls in set(subclasses_of_other_token).union({other_cls}):
                # If you register a Collision with a Token, collisions with subclasses of the token
                # are also registered
                self._pymunk_register_collision_manager(method.__self__, other_subcls, event, method)
            return True

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

        space = self.board.space
        token_id = hash(token.__class__.__name__) % ((sys.maxsize + 1) * 2)
        other_id = hash(other_class.__name__) % ((sys.maxsize + 1) * 2)
        handler = space.add_collision_handler(token_id, other_id)
        handler.data["method"] = getattr(token, method.__name__)
        handler.data["type"] = event
        if event == "begin":
            handler.begin = self.board.pymunk_touching_collision_listener
        if event == "separate":
            handler.separate = self.board.pymunk_separation_collision_listener
