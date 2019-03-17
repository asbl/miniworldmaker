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
        21: "SPACE",
        273: "UP",
        274: "DOWN",
        276: "LEFT",
        275: "RIGHT",
        13: "ENTER",
        304: "L_SHIFT",
        303: "R_SHIFT"
        }


def key_codes_to_keys(key_pressed_list: list):
    keys = []
    for index, item in enumerate(key_pressed_list):
        if item:
            if index in KEYS:
                keys.append(KEYS.get(index))
    return keys
