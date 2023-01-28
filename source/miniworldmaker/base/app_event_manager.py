from collections import deque
from collections.abc import Sequence
from typing import List, Optional

import miniworldmaker.base.app as app_mod
import pygame
from pygame.event import Event
from miniworldmaker.positions import position as board_position
from miniworldmaker.tools import keys


class AppEventManager:

    def __init__(self, app: "app_mod.App"):
        """The event manager consist

        Args:
            app (app.App): _description_
        """
        self.event_queue: deque = deque()
        self.app: "app_mod.App" = app

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
        keys_pressed = []
        event = None
        keys_pressed = self.get_keys()
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
                pos = board_position.Position.create(pygame.mouse.get_pos())
                self.to_event_queue("mouse_motion", pos)
                # key-events
            elif event.type == pygame.KEYUP:
                self.to_event_queue("key_up", keys_pressed)
                for key in keys_pressed:
                    if type(key) == str and key.islower() and key == pygame.key.name(event.key):
                        self.to_event_queue("key_up_" + key, None)
            elif event.type == pygame.KEYDOWN:
                keys_pressed = self.get_keys(event)
                self.to_event_queue("key_down", keys_pressed)
                for key in keys_pressed:
                    if key.islower() and key == pygame.key.name(event.key):
                        self.to_event_queue("key_down_" + key, None)
            if event.type == pygame.VIDEORESIZE or event.type == pygame.VIDEOEXPOSE:
                for container in self.app.container_manager.containers:
                    container.dirty = 1
                self.app.window.add_display_to_repaint_areas()
            # CHECK IF APP SHOULD QUIT
            if "STRG" in keys_pressed and "Q" in keys_pressed:
                self.app.quit()
            # CALL KEY PRESSED EVENT
        if event and pygame.key.get_pressed().count(1) != 0 and not keys_pressed:
            keys_pressed = self.get_keys(event)
        for key in keys_pressed:
            if type(key) == str:
                self.to_event_queue("key_pressed_" + key, None)

        return False

    @staticmethod
    def get_keys(event: Optional[Event] = None) -> List:
        keys_pressed = []
        if pygame.key.get_pressed().count(1) != 0:
            pygame_keys_pressed: Sequence[bool] = pygame.key.get_pressed()
            keys_pressed = keys.key_codes_to_keys(pygame_keys_pressed)
            if event and hasattr(event, "key"):
                key = keys.event_to_key(event.key, keys_pressed)
                if str(key) and len(key) == 1:
                    keys_pressed.append(key)
                else:
                    keys_pressed.append("")
        return keys_pressed

    def put_mouse_down_in_event_queue(self, event):
        """function is called in 'pygame_events_to_event_queue
        """
        pos = board_position.Position.create(pygame.mouse.get_pos())
        if event.button == 1:
            self.to_event_queue("mouse_left", pos)
        if event.button == 3:
            self.to_event_queue("mouse_right", pos)
        if event.button == 4:
            self.to_event_queue("wheel_up", pos)
        if event.button == 5:
            self.to_event_queue("wheel_down", pos)

    def put_mouse_up_in_event_queue(self, event):
        """function is called in 'pygame_events_to_event_queue
        """
        pos = board_position.Position.create(pygame.mouse.get_pos())
        if event.button == 1:
            self.to_event_queue("mouse_left_released", pos)
        if event.button == 3:
            self.to_event_queue("mouse_right_released", pos)
