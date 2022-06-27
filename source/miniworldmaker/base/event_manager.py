import pygame
from collections import deque

import miniworldmaker.base.app as app
import miniworldmaker.tools.keys as keys


class EventManager:

    def __init__(self, app: "app.App"):
        """The event manager consist

        Args:
            app (app.App): _description_
        """
        self.event_queue: deque = deque()
        self.app: "app.App" = app

    def handle_event_queue(self):
        """ Handle the event queue
         This function is called once per mainloop iteration.
         The event_queue is build with `to_event_queue`.
         """
        while self.event_queue:
            element = self.event_queue.pop()
            [ct.handle_event(element[0], element[1]) for ct in self.app.container_manager.containers if ct.is_listening]
        self.event_queue.clear()

    def to_event_queue(self, event, data):
        """Puts an event to the event queue.
        
        It is handled in the handle_event_queue
        """
        self.event_queue.appendleft((event, data))

    def pygame_events_to_event_queue(self):
        """Puts pygame events to event queue. Called in mainloop (App._update) 1/frame.
        
        Iterates over pygame.event.get() and puts events in event queue.
        """
        if pygame.key.get_pressed().count(1) != 0:
            keys_pressed = pygame.key.get_pressed()
            key_codes = keys.key_codes_to_keys(keys_pressed)
            if "STRG" in key_codes and "Q" in key_codes:
                self.app.quit()
            self.to_event_queue("key_pressed", keys.key_codes_to_keys(keys_pressed))
            keys_pressed = keys.key_codes_to_keys(pygame.key.get_pressed())
            for key in keys_pressed:
                self.to_event_queue("key_pressed_" + key, None)
        for event in pygame.event.get():
            # Event: Quit
            if event.type == pygame.QUIT:
                self.app.quit()
            # Event: Mouse-Button Down
            elif event.type == pygame.MOUSEBUTTONUP:
                self.put_mouse_up_in_event_queue(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.put_mouse_down_in_event_queue(event)
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self.to_event_queue("mouse_motion", (pos[0], pos[1]))
                # key-events
            elif event.type == pygame.KEYUP:
                keys_pressed = keys.key_codes_to_keys(pygame.key.get_pressed())
                self.to_event_queue("key_up", keys_pressed)
                for key in keys_pressed:
                    if key.islower() and key == pygame.key.name(event.key):
                        self.to_event_queue("key_up_" + key, None)
            elif event.type == pygame.KEYDOWN:
                keys_pressed = keys.key_codes_to_keys(pygame.key.get_pressed())
                self.to_event_queue("key_down", keys_pressed)
                for key in keys_pressed:
                    if key.islower() and key == pygame.key.name(event.key):
                        self.to_event_queue("key_down_" + key, None)
            if event.type == pygame.VIDEORESIZE:
                self.app.window.add_display_to_repaint_areas()
        return False

    def put_mouse_down_in_event_queue(self, event):
        """function is called in 'pygame_events_to_event_queue
        """
        pos = pygame.mouse.get_pos()
        if event.button == 1:
            self.to_event_queue("mouse_left", (pos[0], pos[1]))
        if event.button == 3:
            self.to_event_queue("mouse_right", (pos[0], pos[1]))
        if event.button == 4:
            self.to_event_queue("wheel_up", (pos[0], pos[1]))
        if event.button == 5:
            self.to_event_queue("wheel_down", (pos[0], pos[1]))

    def put_mouse_up_in_event_queue(self, event):
        """function is called in 'pygame_events_to_event_queue
        """
        pos = pygame.mouse.get_pos()
        if event.button == 1:
            self.to_event_queue("mouse_left_released", (pos[0], pos[1]))
        if event.button == 3:
            self.to_event_queue("mouse_right_released", (pos[0], pos[1]))

    def get_keys(self):
        key_codes = None
        if pygame.key.get_pressed().count(1) != 0:
            keys_pressed = pygame.key.get_pressed()
            key_codes = keys.key_codes_to_keys(keys_pressed)
        return key_codes
