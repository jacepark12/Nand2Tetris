import pathlib
import sys
from typing import List

from hack_assembler.codetmp import comp, dest, jump
from hack_assembler.parser import CommandType, Parser
from hack_assembler.symbol_table import SymbolTable


def should_ignore(line: str) -> bool:
    if line.strip() == "":
        return True
    if line.strip().startswith("//"):
        return True
    return False


def preprocess_lines(lines: List[str]) -> List[str]:
    # if line is empty, skip it
    return [line.strip() for line in lines if should_ignore(line) is False]


def read_file(file_path: pathlib.Path) -> List[str]:
    with open(file_path, "r") as f:
        return f.readlines()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Missing required argument.")

    input_file_path = pathlib.Path(sys.argv[1])
    output_file_path = (
        input_file_path.parent / input_file_path.with_suffix(".hack").name
    )

    lines = read_file(sys.argv[1])
    lines = preprocess_lines(lines)

    parser = Parser(lines=lines)
    symbol_table = SymbolTable()

    rom_index = 0
    ram_index = 16

    while True:
        if parser.has_more_commands is False:
            break
        parser.advance()

        if parser.command_type in [CommandType.A_COMMAND, CommandType.C_COMMAND]:
            rom_index += 1

        if parser.command_type == CommandType.L_COMMAND:
            symbol = parser.symbol
            symbol_table.add_entry(symbol, rom_index)

    outputs = []
    parser.reset()
    while True:
        if parser.has_more_commands is False:
            break
        parser.advance()

        if parser.command_type == CommandType.C_COMMAND:
            c = comp(parser.comp)
            d = dest(parser.dest)
            j = jump(parser.jump)
            output_line = f"111{c:07b}{d:03b}{j:03b}\n"
            outputs.append(output_line)
        elif parser.command_type == CommandType.A_COMMAND:
            symbol = parser.symbol
            if symbol_table.contains(symbol):
                symbol_int = int(symbol_table.get_address(symbol))
            elif symbol.isdecimal():
                symbol_int = int(symbol)
            else:
                symbol_table.add_entry(symbol, ram_index)
                symbol_int = ram_index
                ram_index += 1

            output_line = f"{symbol_int:016b}\n"

            outputs.append(output_line)

    with open(output_file_path, "w") as f:
        f.writelines(outputs)
