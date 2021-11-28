from collections import defaultdict
from inspect import signature
from miniworldmaker.tools.inspection_methods import InspectionMethods


class BoardEventHandler:

    def __init__(self, board):
        self.executed_events: set = set()
        self.board = board

    def handle_event(self, event: str, data):
        """ 
        Call specific event handlers (e.g. "on_mouse_left", "on_mouse_right", ...) for tokens

        Args:
            event: A string-identifier for the event, e.g. `reset`, `setup`, `switch_board`
            data: Data for the event, e.g. the mouse-position, the pressed key, ...
        """
        if event not in self.executed_events:  # events shouldn't be called more than once per tick
            self.executed_events.add(event)
            tokens = self.board.tokens
            all_objects = list(tokens) + [self.board]
            # handle global events
            if event in ["reset"]:
                self.handle_reset_event()
            if event in ["setup"]:
                self.handle_setup_event()
            if event in ["switch_board"]:
                self.handle_switch_board_event(*data)
            # events which can be received by all objects
            for a_object in all_objects:
                if event in ["key_down", "key_pressed", "key_down", "key_up"]:
                    self.handle_key_event(a_object, event, data)
                if event in ["mouse_left", "mouse_right", "mouse_motion"]:
                    self.handle_mouse_event(a_object, event, data)
                if event in ["clicked_left", "clicked_right"]:
                    self.handle_mouse_token_event(a_object, event, data)
                if event in ["message"]:
                    self.handle_message_event(a_object, event, data)
                if event in ["button_pressed"]:
                    self.handle_button_event(a_object, event, data)

    def handle_key_event(self, receiver, event, data):
        # any key down?
        method = InspectionMethods.get_instance_method(receiver, "on_" + str(event))
        if method:
            InspectionMethods.call_instance_method(receiver, method, list([data]))
        # specific key down?
        for key in data:
            if key == key.lower():
                method = InspectionMethods.get_instance_method(receiver, "on_" + event + "_" + key)
                if method:
                    InspectionMethods.call_instance_method(receiver, method, None)

    def handle_mouse_event(self, listener_instance, event, data):
        # any key down?
        method_name = "on_" + event
        method = InspectionMethods.get_instance_method(listener_instance, method_name)
        if method:
            sig = InspectionMethods.get_signature(method, (data,))
            if len(sig.parameters) == 1:
                InspectionMethods.call_instance_method(listener_instance, method, (data,))

    def handle_mouse_token_event(self, instance, event, data):
        # any key down?
        token = data[0]
        position = data[1]
        method_name = "on_" + event
        method = InspectionMethods.get_instance_method(token, method_name)
        if method:
            sig = InspectionMethods.get_signature(method)
            if len(sig.parameters) == 1:
                InspectionMethods.call_instance_method(instance, method, [position])
        tokens = self.board.get_tokens_by_pixel(position)
        for token in tokens:
            method = InspectionMethods.get_instance_method(token, method_name)
            if method:
                InspectionMethods.call_instance_method(instance, method, [position])

    def handle_setup_event(self):
        if not self.board._is_setup:
            if hasattr(self.board, "setup") and callable(getattr(self.board, "setup")):
                self.board.setup()
                self._is_setup = True
            if hasattr(self.board, "on_setup") and callable(getattr(self.board, "on_setup")):
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
        new_board.run()
        return new_board

    def handle_act_event(self, receiver):
        # any key down?
        method = InspectionMethods.get_instance_method(receiver, "act")
        if method:
            InspectionMethods.call_instance_method(receiver, method, None)

    def handle_button_event(self, receiver, event, data):
        # any key down?
        method = InspectionMethods.get_instance_method(receiver, "on_button_pressed")
        if method:
            InspectionMethods.call_instance_method(receiver, method, data)

    def handle_message_event(self, receiver, event, data):
        # any key down?
        method = InspectionMethods.get_instance_method(receiver, "on_message")
        if method:
            InspectionMethods.call_instance_method(receiver, method, (str(data),))
