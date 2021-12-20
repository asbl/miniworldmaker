from miniworldmaker.tools import mwminspection
from miniworldmaker.tools import method_caller
import miniworldmaker
from collections import defaultdict
from typing import Any
from miniworldmaker.tools import keys
import inspect


class BoardEventHandler:
    """Processes Board Events

      * Board Events which can be registered are stored self.events variable.
      * Board Events which are registered are stored in the dict self.registered_events
    """

    def __init__(self, board):
        self.executed_events: set = set()
        self.board = board
        self.registered_events = defaultdict(set)
        self.mouse_events = ["on_mouse_left", "on_mouse_right", "on_mouse_motion"]
        self.clicked_on_token_events = ["on_clicked", "on_clicked_left", "on_clicked_right"]
        self.key_events = ["on_key_down", "on_key_pressed", "on_key_up"]
        self.specific_key_events = []
        for key, value in keys.KEYS.items():
            self.specific_key_events.append("on_key_down_"+value.lower())
            self.specific_key_events.append("on_key_pressed_"+value.lower())
            self.specific_key_events.append("on_key_up_"+value.lower())
        self.message_event = ["on_message"]
        self.act_event = ["act"]
        self.started_event = ["on_started"]
        self.setup_events = ["on_setup", "on_board_loaded"]
        self.border_events = ["on_sensing_borders", "on_sensing_left_border",
                              "on_sensing_right_border", "on_sensing_top_border", "on_sensing_bottom_border"]
        self.on_board_events = ["on_sensing_on_board", "on_sensing_not_on_board"]
        self.events = self.mouse_events + self.specific_key_events + self.key_events + \
            self.clicked_on_token_events + self.message_event + \
            self.act_event + self.border_events + self.on_board_events + self.setup_events + self.started_event
        for event in self.events:
            self.registered_events[event] = set()
        self.register_events_for_board()

    def register_events_for_board(self):
        """Registers all Board events.
        """
        self.register_events(self.setup_events, self.board)
        self.register_events(self.message_event, self.board)
        self.register_events(self.act_event, self.board)
        self.register_events(self.started_event, self.board)
        self.register_events(self.mouse_events, self.board)
        self.register_events(self.key_events, self.board)
        self.register_events(self.specific_key_events, self.board)
        self.register_events(self.specific_key_events, self.board)

    def register_events_for_token(self, token: "miniworldmaker.Token"):
        """Registers all Token events

        Args:
            token : The token, events shoudl be registered to.
        """
        self.register_events(self.message_event, token)
        self.register_events(self.act_event, token)
        self.register_events(self.mouse_events, token)
        self.register_events(self.key_events, token)
        self.register_events(self.clicked_on_token_events, token)
        self.register_events(self.specific_key_events, token)
        self.register_sensing_token_events(token)
        self.register_events(self.border_events, token)
        self.register_events(self.on_board_events, token)

    def register_sensing_token_events(self, instance):
        members = dir(instance)
        for member in (member for member in members if (member.startswith("on_sensing_") or member.startswith("on_not_sensing_")) and member not in self.events):
            method = mwminspection.MWMInspection(instance).get_instance_method(member)
            if method and member.startswith("on_sensing_"):
                self.register_class_method("on_sensing_token", instance, method)
            if method and member.startswith("on_not_sensing_"):
                self.register_class_method("on_not_sensing_token", instance, method)
            
    def register_events(self, events, instance):
        for event in events:
            method = mwminspection.MWMInspection(instance).get_instance_method(event)
            if method:
                self.register_class_method(event, instance, method)

    def register_event(self, event, instance):
        if event in self.events:
            method = mwminspection.MWMInspection(instance).get_instance_method(event)
            if method:
                self.register_custom_method(event, instance, method)
        elif event.startswith("on_sensing_"):
            method = mwminspection.MWMInspection(instance).get_instance_method(event)
            if method:
                self.registered_events["on_sensing_token"].add(method)
        elif event.startswith("on_touching_"):
            method = mwminspection.MWMInspection(instance).get_instance_method(event)
            if method:
                self.board.register_touching_method(method)
        elif event.startswith("on_separation_from_"):
            method = mwminspection.MWMInspection(instance).get_instance_method(event)
            if method:
                self.board.register_separate_method(method)

    def register_custom_method(self, event, instance, method):
        """Register method for event handling. (called in register_event)

        Args:
            event ([str]): The event
            instance: The instance (e.g. board or token)
            method ([type]): The method which should registered as handler for event.
        """
        if method:
            self.registered_events[event].add(method)

    def register_class_method(self, event, instance, method):
        """Register method for event handling (called in register_events)

        Args:
            event ([str]): The event
            instance: The instance (e.g. board or token)
            method ([type]): The method which should registered as handler for event.
        """
        overwritten_methods = {name for name, method in vars(
            instance.__class__).items() if callable(method)}
        parents = inspect.getmro(instance.__class__)
        if instance.__class__ not in [miniworldmaker.Token, miniworldmaker.Board] and method.__name__ in overwritten_methods:
            self.registered_events[event].add(method)
        else:
            parent_overwritten_methods = set()
            for parent in parents:
                if parent.__name__ not in ["object", "Board", "Container", "Sprite", "DirtySprite", "Token", instance.__class__.__name__]:
                    parent_overwritten_methods = parent_overwritten_methods.union(
                        {name for name, method in vars(parent.__class__).items() if callable(method)})
            parent_overwritten_methods = parent_overwritten_methods - overwritten_methods
            if method.__name__ in parent_overwritten_methods:
                self.registered_events[event].add(method)

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
            for method in self.registered_events[event].copy():
                if type(data) in [list, str, tuple]:
                    data = [data]
                method_caller.call_method(method, data, allow_none=False)
        # handle global events
        if event in ["reset"]:
            self.handle_reset_event()
        if event in ["switch_board"]:
            self.handle_switch_board_event(*data)

    def unregister_instance(self, instance):
        awaiting_remove = defaultdict()
        for event, method_set in self.registered_events.items():
            for method in method_set:
                if method.__self__ == instance:
                    awaiting_remove[event] = method
        for event, method in awaiting_remove.items():
            self.registered_events[event].remove(method)

    def act_all(self):
        # acting
        for method in self.registered_events["act"].copy():
            method_caller.call_method(method, None, False)

    def handle_click_on_token_event(self, event, data):
        if event == "mouse_left":
            on_click_methods = self.registered_events["on_clicked_left"].union(
                self.registered_events["on_clicked"])
        else:
            on_click_methods = self.registered_events["on_clicked_right"]
        for method in on_click_methods.copy():
            token = method.__self__
            if token.sensing_point(data):
                method_caller.call_method(method, [data])

    def handle_setup_event(self):
        if not self.board._is_setup:
            self.board.on_setup()
            self.board._is_setup = True
        return self

    def handle_reset_event(self):
        self.board.app.event_manager.event_queue.clear()
        for token in self.board.tokens:
            token.remove()
        self.board.app.board = self.board.__class__(self.board.width, self.board.height)
        self.board.app.board.run()
        board = self.app.board
        board.event_queue.clear()
        return board

    def handle_switch_board_event(self, new_board):
        app = self.board.app
        app.event_manager.event_queue.clear()
        app.board = new_board
        new_board.running = True
        new_board.run(event="board_loaded", )
        return new_board
