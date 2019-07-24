KEYS = {113: "Q",
        119: "W",
        101: "E",
        114: "R",
        116: "T",
        121: "Z",
        117: "U",
        105: "I",
        111: "O",
        112: "P",
        97: "A",
        115: "S",
        100: "D",
        102: "F",
        103: "G",
        104: "H",
        106: "J",
        107: "K",
        108: "L",
        122: "Y",
        120: "X",
        99: "C",
        118: "V",
        98: "B",
        110: "N",
        109: "M",
        32: "SPACE",
        273: "UP",
        274: "DOWN",
        276: "LEFT",
        275: "RIGHT",
        13: "ENTER",
        304: "L_SHIFT",
        303: "R_SHIFT",
        306: "STRG",
        96: "^",
        282: "F1",
        283: "F2",
        284: "F3",
        285: "F4",
        286: "F5",
        287: "F6",
        288: "F7",
        289: "F8",
        290: "F9",
        291: "F10",
        292: "F11",
        27: "ESC",
        }


def key_codes_to_keys(key_pressed_list: list):
    keys = []
    for index, item in enumerate(key_pressed_list):
        if item:
            if index in KEYS:
                keys.append(KEYS.get(index))
                keys.append(KEYS.get(index).lower())
    return keys
