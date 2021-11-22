import pygame
from collections import deque
from inspect import getmembers
from pprint import pprint
from miniworldmaker.tools import keys

class EventManager:
    """ Handles the event queue
    """
    def __init__(self, app):
        self.log_events : str = "None"
        self.event_queue : deque = deque()
        self.app : "App" = app

    def handle_event_queue(self):
        """ Handle the event queue
         This function is called once per mainloop iteration.
         The event_queue is build with `send_event_to_containers`.
         """
        while self.event_queue:
            element = self.event_queue.pop()
            for ct in self.app.container_manager.containers:
                ct.handle_event(element[0], element[1])
        self.event_queue.clear()

    def send_event_to_containers(self, event, data):
        """
        Sends a event to all containers (usually called in process_pygame_events)
        """
        self.event_queue.appendleft((event, data))
    
    def process_pygame_events(self):
        """
        The function is called in App._update once per tick.
        """
        if pygame.key.get_pressed().count(1) != 0:
            keys_pressed = pygame.key.get_pressed()
            key_codes = keys.key_codes_to_keys(keys_pressed)
            if "STRG" in key_codes and "Q" in key_codes:
                self.app.quit()
            self.send_event_to_containers("key_pressed", keys.key_codes_to_keys(keys_pressed))
            self.key_pressed(keys.key_codes_to_keys(keys_pressed))
        for event in pygame.event.get():
            # Event: Quit
            if event.type == pygame.QUIT:
                self.app.quit()
            # Event: Mouse-Button Down
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.send_mouse_down(event)
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self.send_event_to_containers("mouse_motion", (pos[0], pos[1]))
                # key-events
            elif event.type == pygame.KEYUP:
                keys_pressed = keys.key_codes_to_keys(pygame.key.get_pressed())
                self.send_event_to_containers("key_up", keys_pressed)
            elif event.type == pygame.KEYDOWN:
                keys_pressed = keys.key_codes_to_keys(pygame.key.get_pressed())
                self.send_event_to_containers("key_down", keys_pressed)
        return False

    def send_mouse_down(self, event):
        """
        function is called in 'process_pygame_events
        """
        pos = pygame.mouse.get_pos()
        if event.button == 1:
            self.send_event_to_containers("mouse_left", (pos[0], pos[1]))
        if event.button == 3:
            self.send_event_to_containers("mouse_right", (pos[0], pos[1]))
        if event.button == 4:
            self.send_event_to_containers("wheel_up", (pos[0], pos[1]))
        if event.button == 5:
            self.send_event_to_containers("wheel_down", (pos[0], pos[1]))
        for token in self.app.board.tokens:
            if hasattr(token, "on_clicked_left"):
                if token.sensing_point(pos):
                    self.send_event_to_containers("clicked_left", (token, (pos[0], pos[1])))


    def key_pressed(self, key):
        def wrapper_accepting_arguments(key):
            function(key)
        return wrapper_accepting_arguments

    def get_keys(self):
        key_codes = None
        if pygame.key.get_pressed().count(1) != 0:
            keys_pressed = pygame.key.get_pressed()
            key_codes = keys.key_codes_to_keys(keys_pressed)
        return key_codes