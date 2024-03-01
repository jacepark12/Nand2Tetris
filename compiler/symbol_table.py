from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class SymbolKind(Enum):
    STATIC = (0,)
    FIELD = (1,)
    ARG = (2,)
    VAR = 3


@dataclass
class Symbol:
    type: str
    index: int


class Table:
    def __init__(self, kind: SymbolKind):
        self.kind = kind
        self.current_index = 0
        self.table: Dict[str, Symbol] = {}

    @property
    def var_count(self) -> int:
        return len(self.table)

    def define(self, name: str, symbol_type: str) -> None:
        self.table[name] = Symbol(type=symbol_type, index=self.current_index)
        self.current_index += 1

    def has_symbol(self, name: str) -> bool:
        return name in self.table

    def symbol_type(self, name: str) -> str:
        if name not in self.table:
            raise RuntimeError("Undefined symbol name.")
        return self.table[name].type

    def index(self, name: str) -> int:
        if name not in self.table:
            raise RuntimeError("Undefined symbol name.")
        return self.table[name].index


class SymbolTable:

    def __init__(self):
        self.class_table: Dict[SymbolKind, Table] = {
            SymbolKind.STATIC: Table(SymbolKind.STATIC),
            SymbolKind.FIELD: Table(SymbolKind.FIELD),
        }
        self.subroutine_table: Optional[Dict[SymbolKind, Table]] = None

    def start_subroutine(self) -> None:
        self.subroutine_table = {
            SymbolKind.ARG: Table(SymbolKind.ARG),
            SymbolKind.VAR: Table(SymbolKind.VAR),
        }

    def define(self, name: str, symbol_type: str, kind: SymbolKind) -> None:
        if kind in [SymbolKind.STATIC, SymbolKind.FIELD]:
            self.class_table[kind].define(name=name, symbol_type=symbol_type)
        elif kind in [SymbolKind.ARG, SymbolKind.VAR]:
            self.subroutine_table[kind].define(name=name, symbol_type=symbol_type)

    def var_count(self, kind: SymbolKind) -> int:
        if kind in [SymbolKind.STATIC, SymbolKind.FIELD]:
            return self.class_table[kind].var_count
        elif kind in [SymbolKind.ARG, SymbolKind.VAR]:
            return self.subroutine_table[kind].var_count

    def kind_of(self, name: str) -> Optional[SymbolKind]:
        if self.subroutine_table is not None:
            for kind, table in self.subroutine_table.items():
                if table.has_symbol(name):
                    return kind

        for kind, table in self.class_table.items():
            if table.has_symbol(name):
                return kind

        return None

    def type_of(self, name: str) -> Optional[str]:
        if self.subroutine_table is not None:
            for table in self.subroutine_table.values():
                if table.has_symbol(name):
                    return table.symbol_type(name)

        for table in self.class_table.values():
            if table.has_symbol(name):
                return table.symbol_type(name)

        return None

    def index_of(self, name: str) -> Optional[int]:
        if self.subroutine_table is not None:
            for table in self.subroutine_table.values():
                if table.has_symbol(name):
                    return table.index(name)

        for table in self.class_table.values():
            if table.has_symbol(name):
                return table.index(name)

        return None
