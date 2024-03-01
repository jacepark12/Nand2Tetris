from enum import Enum
from typing import List


class CommandType(Enum):
    C_ARITHMETIC = (1,)
    C_PUSH = (2,)
    C_POP = (3,)
    C_LABEL = (4,)
    C_GOTO = (5,)
    C_IF = (6,)
    C_FUNCTION = (7,)
    C_RETURN = (8,)
    C_CALL = 9


class Parser:

    def __init__(self, lines: List[str]):
        self.lines: List[str] = lines
        self.current_line: str = ""
        self.current_line_index: int = -1

    @property
    def has_more_commands(self) -> bool:
        return self.current_line_index < len(self.lines) - 1

    def advance(self) -> None:
        self.current_line_index += 1
        self.current_line = self.lines[self.current_line_index]

    @property
    def command_type(self) -> CommandType:
        args = self.current_line.split(" ")
        if len(args) == 1 and args[0] != "return":
            return CommandType.C_ARITHMETIC
        if len(args) == 1 and args[0] == "return":
            return CommandType.C_RETURN
        if len(args) == 2 and args[0] == "label":
            return CommandType.C_LABEL
        if len(args) == 2 and args[0] == "goto":
            return CommandType.C_GOTO
        if len(args) == 2 and args[0] == "if-goto":
            return CommandType.C_IF
        if len(args) == 3 and args[0] == "function":
            return CommandType.C_FUNCTION
        if len(args) == 3 and args[0] == "call":
            return CommandType.C_CALL
        if len(args) == 3 and args[0] == "push":
            return CommandType.C_PUSH
        if len(args) == 3 and args[0] == "pop":
            return CommandType.C_POP

    @property
    def arg1(self) -> str:
        args = self.current_line.split(" ")
        if self.command_type == CommandType.C_RETURN:
            return ""
        if self.command_type == CommandType.C_ARITHMETIC:
            return args[0]
        return args[1]

    @property
    def arg2(self) -> str:
        args = self.current_line.split(" ")
        if self.command_type not in [
            CommandType.C_PUSH,
            CommandType.C_POP,
            CommandType.C_FUNCTION,
            CommandType.C_CALL,
        ]:
            raise RuntimeError()

        return args[2]
