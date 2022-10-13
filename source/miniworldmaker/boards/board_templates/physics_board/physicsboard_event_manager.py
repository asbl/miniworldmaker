import miniworldmaker.tools.inspection as inspection
from miniworldmaker.boards.board_manager import board_event_manager
from miniworldmaker.tokens import token as token_mod
from miniworldmaker.tools import token_class_inspection


class PhysicsBoardEventManager(board_event_manager.BoardEventManager):
    """Adds on_touching and on separation events
    """

    @classmethod
    def setup_event_list(cls):
        super().setup_event_list()
        touching_token_methods = []
        separation_token_methods = []
        for token_cls in token_class_inspection.TokenClassInspection(token_mod.Token).get_subclasses_for_cls():
            touching_token_methods.append("on_touching_" + token_cls.__name__.lower())
        for token_cls in token_class_inspection.TokenClassInspection(token_mod.Token).get_subclasses_for_cls():
            separation_token_methods.append("on_separation_from_" + token_cls.__name__.lower())
        cls.token_class_events["on_touching"] = touching_token_methods
        cls.token_class_events["on_separation"] = separation_token_methods
        cls.fill_event_sets()

    def register_event(self, member, instance):
        super().register_event(member, instance)
        method = inspection.Inspection(instance).get_instance_method(member)
        if member.startswith("on_touching_"):
            self.board.register_touching_method(method)
        elif member.startswith("on_separation_from_"):
            self.board.register_separate_method(method)
