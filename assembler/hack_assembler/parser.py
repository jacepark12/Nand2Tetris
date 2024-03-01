from enum import Enum
from typing import List


class CommandType(Enum):
    A_COMMAND = 1,
    C_COMMAND = 2,
    L_COMMAND = 3,


class Parser:

    def __init__(self, lines: List[str]):
        self.lines: List[str] = lines
        self.current_line: str = ""
        self.current_line_index: int = -1

    @property
    def has_more_commands(self) -> bool:
        return self.current_line_index < len(self.lines) -1

    def advance(self) -> None:
        self.current_line_index += 1
        self.current_line = self.lines[self.current_line_index]

    def reset(self) -> None:
        self.current_line_index = -1
        self.current_line = ""

    @property
    def command_type(self) -> CommandType:
        if self.current_line.startswith('@'):
            return CommandType.A_COMMAND
        elif self.current_line.startswith('('):
            return CommandType.L_COMMAND
        else:
            return CommandType.C_COMMAND

    @property
    def symbol(self) -> str:
        command_type = self.command_type
        if command_type != CommandType.A_COMMAND and command_type != CommandType.L_COMMAND:
            raise Exception("Command type should be A_Command or L_Command")

        # @Xxx
        if command_type == CommandType.A_COMMAND:
            return self.current_line[1:]
        # (Xxx)
        if command_type == CommandType.L_COMMAND:
            return self.current_line[1:-1]

    @property
    def dest(self) -> str:
        command_type = self.command_type
        if command_type != CommandType.C_COMMAND:
            raise Exception("Command type should be C_Command")

        # dest=comp;JMP
        # comp;JMP
        # dest=comp
        dest = self.current_line.split(";")[0]
        if "=" in self.current_line:
            return dest.split("=")[0]
        else:
            return ""

    # 한번 테스트하기
    @property
    def comp(self) -> str:
        command_type = self.command_type
        if command_type != CommandType.C_COMMAND:
            raise Exception("Command type should be C_Command")

        # dest=comp;JMP
        # comp;JMP
        # dest=comp
        if "=" not in self.current_line:
            return self.current_line.split(";")[0]
        else:
            comp = self.current_line.split("=")[1]
            comp = comp.split(";")[0]
            return comp

    @property
    def jump(self) -> str:
        command_type = self.command_type
        if command_type != CommandType.C_COMMAND:
            raise Exception("Command type should be C_Command")

        # dest=comp;JMP
        # dest;JMP
        # dest
        # dest=comp
        if ';' in self.current_line:
            return self.current_line.split(";")[1]
        else:
            return ''
