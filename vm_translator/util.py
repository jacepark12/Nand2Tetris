import textwrap
from typing import List


def read_file(file_name) -> List[str]:
    with open(file_name, 'r') as f:
        f.readline()
        return f.readlines()


def should_ignore(line: str) -> bool:
    if line.strip() == '':
        return True
    if line.strip().startswith('//'):
        return True
    return False


# remove comment in same line
# ex) if-goto LOOP        // if n > 0, goto LOOP
# preprocess result should be if-goto LOOP
def preprocess_line(line: str) -> str:
    return line.split('//')[0].strip()


def preprocess_lines(lines: List[str]) -> List[str]:
    # if line is empty, skip it
    return [preprocess_line(line) for line in lines if should_ignore(line) is False]
