from enum import Enum
from typing import List


class SegmentEnum(Enum):
    CONST = 0,
    ARG = 1,
    LOCAL = 2,
    STATIC = 3,
    THIS = 4,
    THAT = 5,
    POINTER = 6,
    TEMP = 7


class ArithCommandEnum(Enum):
    ADD = 0,
    SUB = 1,
    NEG = 2,
    EQ = 3,
    GT = 4,
    LT = 5,
    AND = 6,
    OR = 7,
    NOT = 8


def segment_enum_to_str(segment: SegmentEnum) -> str:
    match segment:
        case SegmentEnum.CONST:
            return "constant"
        case SegmentEnum.ARG:
            return "argument"
        case SegmentEnum.LOCAL:
            return "local"
        case SegmentEnum.STATIC:
            return "static"
        case SegmentEnum.THIS:
            return "this"
        case SegmentEnum.THAT:
            return "that"
        case SegmentEnum.POINTER:
            return "pointer"
        case SegmentEnum.TEMP:
            return "temp"

def arith_command_enum_to_str(command: ArithCommandEnum) -> str:
    match command:
        case ArithCommandEnum.ADD:
            return "add"
        case ArithCommandEnum.SUB:
            return "sub"
        case ArithCommandEnum.NEG:
            return "neg"
        case ArithCommandEnum.EQ:
            return "eq"
        case ArithCommandEnum.GT:
            return "gt"
        case ArithCommandEnum.LT:
            return "lt"
        case ArithCommandEnum.AND:
            return "and"
        case ArithCommandEnum.OR:
            return "or"
        case ArithCommandEnum.NOT:
            return "not"

class VMWriter:

    def __init__(self):
        self.output_lines: List[str] = []

    def write_push(self, segment: SegmentEnum, index: int) -> None:
        self.output_lines.append(f"push {segment_enum_to_str(segment)} {index}")

    def write_pop(self, segment: SegmentEnum, index: int) -> None:
        self.output_lines.append(f"pop {segment_enum_to_str(segment)} {index}")

    def write_arithmetic(self, command: ArithCommandEnum) -> None:
        self.output_lines.append(arith_command_enum_to_str(command))

    def write_label(self, label: str) -> None:
        self.output_lines.append(f"label {label}")

    def write_if(self, label: str) -> None:
        self.output_lines.append(f"if-goto {label}")

    def write_goto(self, label: str) -> None:
        self.output_lines.append(f"goto {label}")

    def write_call(self, name: str, n_args: int) -> None:
        self.output_lines.append(f"call {name} {n_args}")
        
    def write_function(self, name: str, n_locals: int) -> None:
        self.output_lines.append(f"function {name} {n_locals}")

        # TODO : check if this should be included
        # for i in range(0, n_locals):
        #     self.output_lines.append(f"{self.write_push(SegmentEnum.LOCAL, i)}")

    def write_return(self) -> None:
        self.output_lines.append("return")
