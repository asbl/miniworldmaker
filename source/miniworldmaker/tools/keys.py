import pygame
from pygame.constants import K_a
KEYS = {20: "Q",
        26: "W",
        8: "E",
        21: "R",
        23: "T",
        28: "Z",
        24: "U",
        12: "I",
        18: "O",
        19: "P",
        4: "A",
        22: "S",
        7: "D",
        9: "F",
        10: "G",
        11: "H",
        13: "J",
        14: "K",
        15: "L",
        29: "Y",
        27: "X",
        6: "C",
        25: "V",
        5: "B",
        17: "N",
        16: "M",
        44: "SPACE",
        82: "UP",
        81: "DOWN",
        80: "LEFT",
        79: "RIGHT",
        40: "ENTER",
        225: "L_SHIFT",
        229: "R_SHIFT",
        224: "STRG",
        58: "F1",
        59: "F2",
        60: "F3",
        61: "F4",
        62: "F5",
        63: "F6",
        64: "F7",
        65: "F8",
        66: "F9",
        67: "F10",
        68: "F11",
        41: "ESC",
        }


def key_codes_to_keys(key_pressed_list: list):
    keys = []
    for index, item in enumerate(key_pressed_list):
        if item:
            if index in KEYS:
                keys.append(KEYS.get(index))
                keys.append(KEYS.get(index).lower())
    return keys

def key_code_to_keys(key_pressed):
    """
    Transforms a pygame key to a key_pressed list
    """
    keys = []
    if key_pressed in KEYS:
        keys.append(KEYS.get(index))
        keys.append(KEYS.get(index).lower())
    return keys