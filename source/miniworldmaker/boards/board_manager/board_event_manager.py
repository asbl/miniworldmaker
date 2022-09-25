import inspect
from collections import defaultdict
from typing import Any

import miniworldmaker.boards.board_base as board_base
import miniworldmaker.tools.inspection as inspection
import miniworldmaker.tools.keys as keys
import miniworldmaker.tools.method_caller as method_caller
from miniworldmaker.positions import position as board_position
from miniworldmaker.boards.board_templates.pixel_board import board
from miniworldmaker.tokens import token as token_mod
from miniworldmaker.tokens import token_base
from miniworldmaker.tools import token_class_inspection


class BoardEventManager:
    """Processes Board Events

    * Board Events which can be registered are stored `self.events` variable.
    * Board Events which are registered are stored in the dict self.registered_events
    """

    class_events = dict()
    class_events_set = set()
    members =  set()
    registered_class_events = defaultdict()
    setup = False

    @staticmethod
    def setup_event_list():
        specific_key_events = []
        for key, value in keys.KEYS.items():
            specific_key_events.append("on_key_down_" + value.lower())
            specific_key_events.append("on_key_pressed_" + value.lower())
            specific_key_events.append("on_key_up_" + value.lower())
        detecting_token_methods = []
        not_detecting_token_methods = []
        for cls in token_class_inspection.TokenClassInspection(token_mod.Token).get_subclasses_for_cls():
            detecting_token_methods.append("on_detecting_" + cls.__name__.lower())
            detecting_token_methods.append("on_sensing_" + cls.__name__.lower())
        for cls in token_class_inspection.TokenClassInspection(token_mod.Token).get_subclasses_for_cls():
            not_detecting_token_methods.append("on_not_detecting_" + cls.__name__.lower())
            not_detecting_token_methods.append("on_not_sensing_" + cls.__name__.lower())

        BoardEventManager.class_events = {
            "mouse": ["on_mouse_left",
                      "on_mouse_right",
                      "on_mouse_motion",
                      "on_mouse_left_release",
                      "on_mouse_right_released"
                      ],
            "clicked_on_token": ["on_clicked",
                                 "on_clicked_left",
                                 "on_clicked_right"],
            "key": ["on_key_down",
                    "on_key_pressed",
                    "on_key_up",
                    ],
            "specific_key": specific_key_events,
            "message": ["on_message"],
            "act": ["act"],
            # "setup": ["on_setup"],
            "border": [
                "on_detecting_borders",
                "on_detecting_left_border",
                "on_detecting_right_border",
                "on_detecting_top_border",
                "on_detecting_bottom_border",
            ],
            "on_the_board": ["on_detecting_board",
                             "on_not_detecting_board",
                             "on_sensing_on_board",
                             "on_sensing_not_on_board"],
            "on_detecting": ["on_detecting", "on_detecting_"] + detecting_token_methods,
            "on_not_detecting": ["on_not_detecting", "on_not_detecting_", ] + not_detecting_token_methods
        }
        BoardEventManager.class_events_set = set()
        for key in BoardEventManager.class_events.keys():
            for event in BoardEventManager.class_events[key]:
                BoardEventManager.class_events_set.add(event)

    def __init__(self, board):
        """Events are registered here in multiple event lists.
        The lists are merged into ``self.events``.
        """
        BoardEventManager.setup_event_list()  # setup static event set/dict
        self.executed_events: set = set()
        self.board = board
        self.registered_events = defaultdict(set)
        BoardEventManager.members = self._get_members_for_instance(board)
        self.register_events_for_board(board)

    def _get_members_for_instance(self, instance) -> set:
        """Get"""
        if instance.__class__ not in [token_base.BaseToken,
                                      token_mod.Token,
                                      board_base.BaseBoard,
                                      ]:
            members = {name for name, method in vars(instance.__class__).items() if callable(method)}
            member_set = set([member for member in members if member.startswith("on_") or member.startswith("act")])
            return member_set.union(self._get_members_for_classes(instance.__class__.__bases__))
        else:
            return set()

    def _get_members_for_classes(self, classes) -> set:
        """Get all members for a list of classes

        called recursively in `_get_members for instance` to get all parent class members
        :param classes:
        :return:
        """
        all_members = set()
        for cls in classes:
            if cls not in [token_base.BaseToken,
                           token_mod.Token,
                           board_base.BaseBoard,
                           ]:
                members = {name for name, method in vars(cls).items() if callable(method)}
                member_set = set([member for member in members if member.startswith("on_") or member.startswith("act")])
                member_set.union(self._get_members_for_classes(cls.__bases__))
                all_members = all_members.union(member_set)
            else:
                all_members = set()
        return all_members

    def register_events_for_board(self, board):
        """Registers all Board events."""
        for member in self.members:
            if member in BoardEventManager.class_events_set:
                self.register_event(member, board)

    def register_events_for_token(self, token):
        """Registers all Board events."""
        members = token._event_manager.get_members(token)
        for member in members:
            self.register_event(member, token)

    def get_parent_methods(self, instance):
        parents = inspect.getmro(instance.__class__)
        methods = set()
        for parent in parents:
            if parent in [
                board.Board,
                token_mod.Token,
                token_base.BaseToken
            ]:
                methods = methods.union({method for name, method in vars(parent).items() if callable(method)})
        return methods

    def register_event(self, member, instance):
        method = inspection.Inspection(instance).get_instance_method(member)
        if method:
            for event in BoardEventManager.class_events_set:
                if member == event:
                    self.registered_events[event].add(method)
                    return
            for event in BoardEventManager.class_events_set:
                if member.startswith(event):
                    self.registered_events[event].add(method)
                    return
            if member.startswith("on_touching_"):
                self.board.register_touching_method(method)
            elif member.startswith("on_separation_from_"):
                self.board.register_separate_method(method)


    def handle_event(self, event: str, data: Any):
        """Call specific event handlers (e.g. "on_mouse_left", "on_mouse_right", ...) for tokens

        Args:
            event: A string-identifier for the event, e.g. `reset`, `setup`, `switch_board`
            data: Data for the event, e.g. the mouse-position, the pressed key, ...
        """
        if event in self.executed_events:
            return  # events shouldn't be called more than once per tick
        self.executed_events.add(event)
        if event in ["mouse_left", "mouse_right", "mouse_motion"]:
            self.handle_click_on_token_event(event, data)
        event = "on_" + event
        if event in self.registered_events:
            registered_events = self.registered_events[event].copy()
            for method in registered_events:
                if type(data) in [list, str, tuple, board_position.Position]:
                    data = [data]
                method_caller.call_method(method, data, allow_none=False)
            registered_events.clear()
            del registered_events

    def unregister_instance(self, instance):
        awaiting_remove = defaultdict()
        for event, method_set in self.registered_events.items():
            for method in method_set:
                if method.__self__ == instance:
                    awaiting_remove[event] = method
        for event, method in awaiting_remove.items():
            self.registered_events[event].remove(method)

    def act_all(self):
        registered_act_methods = self.registered_events["act"].copy()
        # acting
        for method in registered_act_methods:
            method_caller.call_method(method, None, False)
        del registered_act_methods

    def handle_click_on_token_event(self, event, data):
        if event == "mouse_left":
            on_click_methods = self.registered_events["on_clicked_left"].union(self.registered_events["on_clicked"]).copy()
        else:
            on_click_methods = self.registered_events["on_clicked_right"].copy()
        for method in on_click_methods:
            token = method.__self__
            if token.detect_point(data):
                method_caller.call_method(method, (data,))
        del on_click_methods
