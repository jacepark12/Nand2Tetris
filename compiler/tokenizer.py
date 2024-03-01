from enum import Enum
from typing import List, Optional, TextIO, Type


class IndexRange:
    def __init__(self, *, start: Optional[int], end: Optional[int]):
        self.start = start
        self.end = end

    def __contains__(self, index):
        if self.start is None or self.end is None:
            return False
        if self.start <= index and index <= self.end:
            return True
        return False


def is_in_index_ranges(index:int, index_ranges: List[IndexRange]):
    for index_range in index_ranges:
        if index in index_range:
            return True
    return False


class TokenType(str, Enum):
    keyword = 'keyword',
    symbol = 'symbol',
    integer_constant = 'integerConstant',
    string_constant = 'stringConstant',
    identifier = 'identifier'


class KeywordEnum(Enum):
    CLASS = 'class'
    CONSTRUCTOR = 'constructor'
    FUNCTION = 'function'
    METHOD = 'method'
    FIELD = 'field'
    STATIC = 'static'
    VAR = 'var'
    INT = 'int'
    CHAR = 'char'
    BOOLEAN = 'boolean'
    VOID = 'void'
    TRUE = 'true'
    FALSE = 'false'
    NULL = 'null'
    THIS = 'this'
    LET = 'let'
    DO = 'do'
    IF = 'if'
    ELSE = 'else'
    WHILE = 'while'
    RETURN = 'return'


class SymbolEnum(Enum):
    OPEN_BRACE = '{'
    CLOSE_BRACE = '}'
    OPEN_PAREN = '('
    CLOSE_PAREN = ')'
    OPEN_BRACKET = '['
    CLOSE_BRACKET = ']'
    DOT = '.'
    COMMA = ','
    SEMICOLON = ';'
    PLUS = '+'
    MINUS = '-'
    ASTERISK = '*'
    SLASH = '/'
    AMPERSAND = '&'
    PIPE = '|'
    LESS_THAN = '<'
    GREATER_THAN = '>'
    EQUAL = '='
    TILDE = '~'


class OtherTokenEnum(Enum):
    INTEGER_CONSTANT = 0,
    STRING_CONSTANT = 1,
    IDENTIFIER = 2


def is_value_in_enum(value: str, enum: Type[Enum]) -> bool:
    return any(value == item.value for item in enum)


def format_value(value: str) -> str:
    if value == "<":
        return "&lt;"
    elif value == ">":
        return "&gt;"
    elif value == "\"":
        return "&quot;"
    elif value == "&":
        return "&amp;"
    else:
        return value


class Token:
    def __init__(self, value: str, type: TokenType):
        self.value = value
        self.type = type


def check_type(input: str) -> TokenType:
    if is_value_in_enum(input, KeywordEnum):
        return TokenType.keyword
    elif is_value_in_enum(input, SymbolEnum):
        return TokenType.symbol
    elif input.isdecimal():
        return TokenType.integer_constant
    elif input.startswith("\""):
        if input.endswith("\""):
            return TokenType.string_constant
        else:
            raise RuntimeError("\" was found at ?")
    else:
        return TokenType.identifier


class Tokenizer:

    # TODO : Do not read whole file in init
    def __init__(self, f: TextIO):
        self.file_io = f
        self.tokens: List[Token] = []
        self.current_token: Optional[Token] = None
        self.index = -1

        buffer: str = ""
        token_stack: List[str] = []

        # Push tokens to token_stack. Split with space or new line.
        token_str = ""
        reading_constant: bool = False
        for ch in iter(lambda: f.read(1), ''):
            if ch == "\"":
                if reading_constant is False:
                    token_stack.append(token_str.strip())
                    token_str = ""
                    reading_constant = True
                elif reading_constant is True:
                    token_stack.append("\"" + token_str + "\"")
                    token_str = ""
                    reading_constant = False
            elif reading_constant is True:
                token_str += ch
            elif ch not in [" ", "\n"]:
                token_str += ch
            elif ch == "\n":
                token_stack.append(token_str.strip())
                token_stack.append("\n")
                token_str = ""
            elif ch == " ":
                if len(token_str) > 0:
                    token_stack.append(token_str.strip())
                    token_str = ""

        token_stack.append(token_str)

        # Iterate token_stack and find index of ranges to be ignored.
        # Comment Type 1 -> // | ///
        # Comment Type 2 -> /**
        comment_type: Optional[int] = None
        comment_index_ranges: List[IndexRange] = []
        for idx, token in enumerate(token_stack):

            if token == "//" or token == "///":
                comment_index_ranges.append(IndexRange(start=idx, end=None))
                comment_type = 1
            elif token == "/**":
                comment_index_ranges.append(IndexRange(start=idx, end=None))
                comment_type = 2
            elif token == "\n":
                if comment_type == 1:
                    comment_index_ranges[-1].end = idx
                    comment_type = None
            elif token == "*/":
                if comment_type == 2:
                    comment_index_ranges[-1].end = idx
                    comment_type = None

        # 이제 저장된 토큰을 처리한다.
        for idx, token in enumerate(token_stack):
            if is_in_index_ranges(idx, comment_index_ranges):
                continue
            if token in ["\n", ""]:
                continue
            if token[0] == "\"":
                self.tokens.append(Token(token[1:-1], TokenType.string_constant))
                continue
            for ch in token:
                if is_value_in_enum(ch, SymbolEnum):
                    if len(buffer) > 0:
                        self.tokens.append(Token(buffer, check_type(buffer)))
                    self.tokens.append(Token(ch, TokenType.symbol))
                    buffer = ""
                else:
                    buffer += ch
            if len(buffer) > 0:
                self.tokens.append(Token(buffer, check_type(buffer)))
                buffer = ""

    def has_more_token(self) -> bool:
        return self.index < len(self.tokens) - 1

    def advance(self) -> None:
        self.index += 1
        self.current_token = self.tokens[self.index]

    def previous(self, previous_index) -> None:
        if self.index - previous_index < 0:
            raise RuntimeError("Index out of range")
        self.index -= previous_index
        self.current_token = self.tokens[self.index]

    def token_type(self) -> TokenType:
        if self.current_token is None:
            raise RuntimeError("Current token not set!")
        return self.current_token.type

    def keyword(self) -> KeywordEnum:
        if self.current_token is None or self.current_token.type is not TokenType.keyword:
            raise RuntimeError("Current token is not keyword type.")
        return KeywordEnum(self.current_token.value)

    def symbol(self) -> SymbolEnum:
        if self.current_token is None or self.current_token.type is not TokenType.symbol:
            raise RuntimeError("Current token is not symbol type.")
        return SymbolEnum(self.current_token.value)

    def identifier(self) -> str:
        if self.current_token is None or self.current_token.type is not TokenType.identifier:
            raise RuntimeError("Current token is not identifier type.")
        return self.current_token.value

    def int_val(self) -> int:
        if self.current_token is None or self.current_token.type is not TokenType.integer_constant:
            raise RuntimeError("Current token is not integer_constant type.")
        return int(self.current_token.value)

    def string_val(self) -> str:
        if self.current_token is None or self.current_token.type is not TokenType.string_constant:
            raise RuntimeError("Current token is not string_constant type.")
        return self.current_token.value

    # TODO : rename method
    def write_xml(self, output_path: str):
        with open(output_path, 'w') as f:
            f.write("<tokens>\n")
            for token in self.tokens:
                xml_string = f"<{token.type.value}> {format_value(token.value)} </{token.type.value}>\n"
                f.write(xml_string)
            f.write("</tokens>\n")
