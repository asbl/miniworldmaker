import collections
import inspect
from collections import defaultdict
from typing import Any
import pygame
import miniworldmaker.boards.board_base as board_base
import miniworldmaker.tools.inspection as inspection
import miniworldmaker.tools.keys as keys
import miniworldmaker.tools.method_caller as method_caller
from miniworldmaker.boards.board_templates.pixel_board import board as board_mod
from miniworldmaker.positions import position as board_position
from miniworldmaker.tokens import token as token_mod
from miniworldmaker.tokens import token_base
from miniworldmaker.tools import token_class_inspection


class BoardEventManager:
    """Processes Board Events

    * Board Events which can be registered are stored `self.events` variable.
    * Board Events which are registered are stored in the dict self.registered_events
    """

    token_class_events = dict()
    token_class_events_set = set()
    board_class_events = dict()
    board_class_events_set = set()
    class_events = dict()
    class_events_set = set()
    members = set()
    registered_class_events = defaultdict()
    setup = False

    @classmethod
    def setup_event_list(cls):
        specific_key_events = []
        for key, value in keys.KEYS.items():
            specific_key_events.append("on_key_down_" + value.lower())
            specific_key_events.append("on_key_pressed_" + value.lower())
            specific_key_events.append("on_key_up_" + value.lower())
        detecting_token_methods = []
        not_detecting_token_methods = []
        for token_cls in token_class_inspection.TokenClassInspection(token_mod.Token).get_subclasses_for_cls():
            detecting_token_methods.append("on_detecting_" + token_cls.__name__.lower())
            detecting_token_methods.append("on_sensing_" + token_cls.__name__.lower())
        for token_cls in token_class_inspection.TokenClassInspection(token_mod.Token).get_subclasses_for_cls():
            not_detecting_token_methods.append("on_not_detecting_" + token_cls.__name__.lower())
            not_detecting_token_methods.append("on_not_sensing_" + token_cls.__name__.lower())

        cls.token_class_events = {
            "mouse": ["on_mouse_left",
                      "on_mouse_right",
                      "on_mouse_motion",
                      "on_mouse_left_released",
                      "on_mouse_right_released"
                      ],
            "clicked_on_token": ["on_clicked",
                                 "on_clicked_left",
                                 "on_clicked_right",
                                 "on_pressed_left"
                                 ],
            "mouse_over": ["on_mouse_over",
                           "on_mouse_leave",
                           "on_mouse_enter"],
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

        cls.board_class_events = {
            "mouse": ["on_mouse_left",
                      "on_mouse_right",
                      "on_mouse_motion",
                      "on_mouse_left_released",
                      "on_mouse_right_released"
                      ],
            "key": ["on_key_down",
                    "on_key_pressed",
                    "on_key_up",
                    ],
            "specific_key": specific_key_events,
            "message": ["on_message"],
            "act": ["act"],
        }
        # Generate
        cls.fill_event_sets()

    @classmethod
    def fill_event_sets(cls):
        cls.class_events = {**cls.token_class_events, **cls.board_class_events}
        cls.token_class_events_set = set()
        for key in cls.token_class_events.keys():
            for event in cls.token_class_events[key]:
                cls.token_class_events_set.add(event)
        cls.board_class_events_set = set()
        for key in cls.board_class_events.keys():
            for event in cls.board_class_events[key]:
                cls.board_class_events_set.add(event)
        cls.class_events_set = set()
        for key in cls.class_events.keys():
            for event in cls.class_events[key]:
                cls.class_events_set.add(event)

    def __init__(self, board):
        self.__class__.setup_event_list()  # setup static event set/dict
        self.executed_events: set = set()
        self.board = board
        self.registered_events = defaultdict(set)
        self.__class__.members = self._get_members_for_instance(board)
        self.register_events_for_board(board)

    def _get_members_for_instance(self, instance) -> set:
        """Gets all members of an instance

        Gets members from instance class and instance base classes
        """
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
        for member in self._get_members_for_instance(board):
            if member in self.__class__.board_class_events_set:  # static
                self.register_event(member, board)


    def register_events_for_token(self, token):
        """Registers all Board events."""
        for member in self._get_members_for_instance(token):
            self.register_event(member, token)

    def get_parent_methods(self, instance):
        parents = inspect.getmro(instance.__class__)
        methods = set()
        for parent in parents:
            if parent in [
                board_mod.Board,
                token_mod.Token,
                token_base.BaseToken
            ]:
                methods = methods.union({method for name, method in vars(parent).items() if callable(method)})
        return methods

    def register_event(self, member, instance):
        """Register event to event manager, IF method exists in instance.

        :param member: the method to register
        :param instance: the instance the method should be registered to (e.g. a board or a token
        """
        method = inspection.Inspection(instance).get_instance_method(member)
        if method:
            for event in self.__class__.class_events_set:
                if member == event:
                    self.registered_events[event].add(method)
                    return event, method
            # needed for detecting_CLASS_Y methods @TODO: Maybe nod needed anymore
            for event in self.__class__.class_events_set:
                if member.startswith(event):
                    self.registered_events[event].add(method)
                    return event, method
        return

    def handle_event(self, event: str, data: Any):
        """Call specific event handlers (e.g. "on_mouse_left", "on_mouse_right", ...) for tokens

        Args:
            event: A string-identifier for the event, e.g. `reset`, `setup`, `switch_board`
            data: Data for the event, e.g. the mouse-position, the pressed key, ...
        """
        if event in self.executed_events:
            return  # events shouldn't be called more than once per tick
        self.executed_events.add(event)
        if event in ["mouse_left", "mouse_right"]:
            self.handle_click_on_token_event(event, data)
        if event in ["mouse_motion"]:
            self.handle_mouse_over_event(event, data)
            self.handle_mouse_enter_event(event, data)
            self.handle_mouse_leave_event(event, data)
        event = "on_" + event
        if event in self.registered_events:
            registered_events = self.registered_events[event].copy()
            for method in registered_events:
                if type(data) in [list, str, tuple, board_position.Position]:
                    if type(data) == board_position.Position and not self.board.rect.collidepoint(data):
                        return
                    data = [data]
                method_caller.call_method(method, data, allow_none=False)
            registered_events.clear()
            del registered_events

    def unregister_instance(self, instance) -> collections.defaultdict:
        """unregisteres an instance (e.g. a Token) from
        event manager.
        """
        unregister_methods_dict = defaultdict()
        for event, method_set in self.registered_events.items():
            for method in method_set:
                if method.__self__ == instance:
                    unregister_methods_dict[event] = method
        for event, method in unregister_methods_dict.items():
            self.registered_events[event].remove(method)
        return unregister_methods_dict

    def act_all(self):
        registered_act_methods = self.registered_events["act"].copy()
        # acting
        for method in registered_act_methods:
            # act method
            instance = method.__self__
            if instance._is_acting :
                method_caller.call_method(method, None, False)
        mouse_pos = pygame.mouse.get_pos()
        self.handle_mouse_pressed("on_pressed_left", mouse_pos)
        del registered_act_methods


    def handle_click_on_token_event(self, event, data):
        if not self.board.is_in_container(data):
            return False
        pos = self.board.camera.get_global_coordinates_for_board(data)
        # get window mouse pos
        if event == "mouse_left":
            on_click_methods = self.registered_events["on_clicked_left"].union(
                self.registered_events["on_clicked"]).copy()
        else:
            on_click_methods = self.registered_events["on_clicked_right"].union(
                self.registered_events["on_clicked"]).copy()
        for method in on_click_methods:
            token = method.__self__
            if token.detect_point(pos):
                method_caller.call_method(method, (data,))
        del on_click_methods

    def handle_mouse_over_event(self, event, data):
        if not self.board.is_in_container(data):
            return False
        pos = self.board.camera.get_global_coordinates_for_board(data) # get global mouse pos by window
        mouse_over_methods = self.registered_events["on_mouse_over"].copy()
        for method in mouse_over_methods:
            token = method.__self__
            if token.detect_point(pos):
                method_caller.call_method(method, (data,))
        del mouse_over_methods

    def handle_mouse_leave_event(self, event, data):
        if not self.board.is_in_container(data):
            return False
        pos = self.board.camera.get_global_coordinates_for_board(data)
        mouse_over_methods = self.registered_events["on_mouse_leave"].copy()
        for method in mouse_over_methods:
            token = method.__self__
            if not hasattr(token, "_mouse_over"):
                token._mouse_over = False
            if not token.detect_point(pos) and token._mouse_over:
                method_caller.call_method(method, (data,))
                token._mouse_over = False
            else:
                token._mouse_over = True
        del mouse_over_methods

    def handle_mouse_enter_event(self, event, data):
        if not self.board.is_in_container(data):
            return False
        pos = self.board.camera.get_global_coordinates_for_board(data)
        mouse_over_methods = self.registered_events["on_mouse_enter"].copy()
        for method in mouse_over_methods:
            token = method.__self__
            if not hasattr(token, "_mouse_over"):
                token._mouse_over = False
            if token.detect_point(pos) and not token._mouse_over:
                method_caller.call_method(method, (data,))
                token._mouse_over = True
            else:
                token._mouse_over = False
        del mouse_over_methods

    def handle_mouse_pressed(self, event, data):
        if not self.board.is_in_container(data):
            return False
        pos = self.board.camera.get_global_coordinates_for_board(data)
        mouse_pressed_methods = self.registered_events["on_pressed_left"].copy()
        for method in mouse_pressed_methods:
            token = method.__self__
            if token.detect_point(pos) and pygame.mouse.get_pressed()[0]:
                method_caller.call_method(method, (pos,))
        del mouse_pressed_methods
