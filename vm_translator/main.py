import pathlib
import sys
from typing import List, Optional

from code_writer import END_LINES, CodeWriter
from jack_parser import CommandType, Parser
from util import preprocess_lines, read_file

TARGET_SUFFIX = ".vm"


class VMTranslator:
    def __init__(self):
        self.code_writer = CodeWriter()
        self._target_path: Optional[pathlib.Path] = None
        self._target_files: List[pathlib.Path] = []
        self.output_path: Optional[pathlib.Path] = None

    @property
    def target_path(self) -> Optional[pathlib.Path]:
        return self._target_path

    @target_path.setter
    def target_path(self, path) -> None:
        if path.is_file() and path.suffix == TARGET_SUFFIX:
            self._target_files.append(path)
            self.output_path = path.with_suffix(".asm")
        elif path.is_dir():
            self.output_path = path / f"{path.name}.asm"
            for file_path in path.glob("*.vm"):
                self._target_files.append(file_path)

    def _generate_asm_code(self, path: pathlib.Path):
        self.code_writer.file_name = path.name.removesuffix(".vm")

        lines = read_file(path)
        lines = preprocess_lines(lines)

        parser = Parser(lines=lines)

        while True:
            h = parser.has_more_commands
            if h is False:
                break
            parser.advance()

            command_type = parser.command_type

            if command_type == CommandType.C_ARITHMETIC:
                self.code_writer.write_arithmetic(parser.arg1)
            elif command_type == CommandType.C_PUSH:
                self.code_writer.write_push_pop("push", parser.arg1, int(parser.arg2))
            elif command_type == CommandType.C_POP:
                self.code_writer.write_push_pop("pop", parser.arg1, int(parser.arg2))
            elif command_type == CommandType.C_LABEL:
                self.code_writer.write_label(parser.arg1)
            elif command_type == CommandType.C_GOTO:
                self.code_writer.write_goto(parser.arg1)
            elif command_type == CommandType.C_IF:
                self.code_writer.write_if(parser.arg1)
            elif command_type == CommandType.C_FUNCTION:
                self.code_writer.write_function(parser.arg1, int(parser.arg2))
            elif command_type == CommandType.C_CALL:
                self.code_writer.write_call(parser.arg1, int(parser.arg2))
            elif command_type == CommandType.C_RETURN:
                self.code_writer.write_return()

    def generate_code(self):
        for target_file in self._target_files:
            self._generate_asm_code(target_file)

    def close(self):
        self.code_writer.output_lines.extend(END_LINES)
        with open(self.output_path, "w") as f:
            f.writelines(self.code_writer.output_lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Missing required argument. Pass path to compile.")
    target_path = pathlib.Path(sys.argv[1])

    vm_translator = VMTranslator()
    vm_translator.target_path = target_path
    vm_translator.generate_code()
    vm_translator.close()
