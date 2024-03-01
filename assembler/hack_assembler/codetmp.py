from typing import Dict

dest_map: Dict[str, int] = {
    'null': 0,
    'M': 1,
    'D': 2,
    'MD': 3,
    'A': 4,
    'AM': 5,
    'AD': 6,
    'AMD': 7
}

jump_map: Dict[str, int] = {
    'null': 0,
    'JGT': 1,
    'JEQ': 2,
    'JGE': 3,
    'JLT': 4,
    'JNE': 5,
    'JLE': 6,
    'JMP': 7
}

comp_map1: Dict[str, int] = {
    '0': 42,
    '1': 63,
    '-1': 58,
    'D': 12,
    'A': 48,
    '!D': 13,
    '!A': 49,
    '-D': 15,
    '-A': 51,
    'D+1': 31,
    'A+1': 55,
    'D-1': 14,
    'A-1': 50,
    'D+A': 2,
    'D-A': 19,
    'A-D': 7,
    'D&A': 0,
    'D|A': 21,
}

comp_map2: Dict[str, int] = {
    'M': 48 + 64,
    '!M': 49 + 64,
    '-M': 51 + 64,
    'M+1': 55 + 64,
    'M-1': 50 + 64,
    'D+M': 2 + 64,
    'D-M': 19 + 64,
    'M-D': 7 + 64,
    'D&M': 0 + 64,
    'D|M': 21 + 64
}


def comp(command: str) -> int:
    if command == "":
        return 0
    if command in comp_map1.keys():
        return comp_map1[command]
    if command in comp_map2.keys():
        return comp_map2[command]
    return 0


def dest(command: str) -> int:
    if command == "":
        return dest_map['null']
    if command in dest_map.keys():
        return dest_map[command]
    return 0


def jump(command: str) -> int:
    if command == "":
        return jump_map['null']
    if command in jump_map.keys():
        return jump_map[command]
    return 0
