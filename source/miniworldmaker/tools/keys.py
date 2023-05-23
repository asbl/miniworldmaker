from collections.abc import Sequence
from typing import List

import pygame

KEYS = {pygame.K_LSHIFT : "L_SHIFT",
        pygame.K_RSHIFT: "R_SHIFT",
        pygame.K_LCTRL: "L_CTRL",
        pygame.K_RCTRL: "R_CTRL",
        pygame.K_BACKSPACE: "BACKSPACE",
        pygame.K_RETURN: "RETURN",
        pygame.K_TAB: "TAB",
        pygame.K_F1: "F1",
        pygame.K_F2: "F2",
        pygame.K_F3: "F3",
        pygame.K_F4: "F4",
        pygame.K_F5: "F5",
        pygame.K_F6: "F6",
        pygame.K_F7: "F7",
        pygame.K_F8: "F8",
        pygame.K_F9: "F9",
        pygame.K_F10: "F10",
        pygame.K_F11: "F11",
        pygame.K_ESCAPE: "ESC",
        pygame.K_DELETE: "DELETE",
        pygame.K_UP: "UP",
        pygame.K_DOWN: "DOWN",
        pygame.K_LEFT: "LEFT",
        pygame.K_RIGHT: "RIGHT",
        pygame.K_UP: "UP",
        pygame.K_DOWN: "DOWN",
        }

mwm_aliases = {
    "return": "ENTER",
    "space": "SPACE",
    "backspace": "BACKSPACE",
}

mwm_strings = {
    "SPACE": " ",
}

def key_codes_to_keys(key_pressed_list: Sequence) -> List:
    keys = []
    print(key_pressed_list)
    for index, item in enumerate(key_pressed_list):
        if item:
            if index in KEYS:
                keys.append(KEYS.get(index))
                keys.append(KEYS.get(index).lower())
    return keys

def key_code_to_key(key_code) -> str:
    if key_code in KEYS:
        return KEYS[key_code]
    else:
        return None
    
def get_key(unicode, keycode):
    if unicode:
        return unicode
    else:
        return key_code_to_key(keycode)
