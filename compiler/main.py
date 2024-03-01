import pathlib
import sys
from enum import Enum
from typing import List, Optional

from compiler.compile_engine import CompileEngine, IdentifierCategory, TreeElement
from compiler.symbol_table import SymbolKind, SymbolTable
from compiler.tokenize_writer import TokenizeWriter
from compiler.vm_writer import ArithCommandEnum, SegmentEnum, VMWriter

TARGET_SUFFIX = ".jack"


class JackCompilerModeEnum(Enum):
    TOKEN_ANALYZE = (0,)
    COMPILE = (1,)


class SubroutineTypeEnum(Enum):
    FUNC = (0,)
    METHOD = (1,)
    CONSTRUCTOR = 2


class CalledSubroutineTypeEnum(Enum):
    FUNC = (0,)
    METHOD = (1,)
    SAME_CLASS_METHOD = (2,)


class JackCompiler:
    def __init__(
        self, mode: Optional[JackCompilerModeEnum] = JackCompilerModeEnum.COMPILE
    ):
        self.mode = mode
        self._target_path: Optional[pathlib.Path] = None
        self._target_files: List[pathlib.Path] = []
        self.xml_output_dir: Optional[pathlib.Path] = None
        self.compile_output_dir: Optional[pathlib.Path] = None
        self.compile_engine: Optional[CompileEngine] = None
        # class attributes for writing VM language
        self.symbol_table: Optional[SymbolTable] = None
        self.class_name: str = ""
        self.vm_writer: Optional[VMWriter] = None
        self.label_count: int = 0
        self.class_var_dec_count: int = 0

    @property
    def target_path(self) -> Optional[pathlib.Path]:
        return self._target_path

    @target_path.setter
    def target_path(self, path) -> None:

        if path.is_file() and path.suffix == TARGET_SUFFIX:
            self.xml_output_dir = path.parent / "xml_output"
            self.compile_output_dir = path.parent / "compile_output"
            self._target_files.append(path)
        elif path.is_dir():
            self.xml_output_dir = path / "xml_output"
            self.compile_output_dir = path / "compile_output"
            for file_path in path.glob("*.jack"):
                self._target_files.append(file_path)

    def analyze_token(self) -> None:

        if self.xml_output_dir.exists() is False:
            self.xml_output_dir.mkdir(parents=True, exist_ok=True)

        for target_file in self._target_files:
            output_path = self.xml_output_dir / target_file.with_suffix(".xml").name
            if output_path is None:
                continue
            self.compile_engine = CompileEngine(file_path=target_file)
            self.compile_engine.start_compile()
            tokenize_writer = TokenizeWriter(
                compiled_tree=self.compile_engine.compiled_tree
            )
            tokenize_writer.write_to_xml(
                output_path=str(output_path),
            )

    def compile(self) -> None:
        if self.compile_output_dir.exists() is False:
            self.compile_output_dir.mkdir(parents=True, exist_ok=True)

        for target_file in self._target_files:
            output_path = self.compile_output_dir / target_file.with_suffix(".vm").name
            if output_path is None:
                continue
            self.compile_engine = CompileEngine(file_path=target_file)
            self.compile_engine.start_compile()
            self._write_vm(output_path=str(output_path))

    def _write_vm_init(self) -> None:
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter()
        self.class_name = ""
        self.label_count = 0
        self.class_var_dec_count = 0

    def _write_vm(self, output_path: str) -> None:
        self._write_vm_init()

        compiled_tree = self.compile_engine.compiled_tree

        for child in compiled_tree.root.children:
            self.handle_element(child)

        with open(output_path, "w") as f:
            for line in self.vm_writer.output_lines:
                f.write(f"{line}\n")

    def handle_element(self, tree_element: TreeElement) -> None:

        if tree_element.visited:
            return

        parent = tree_element.parent
        element_value = tree_element.value
        element_type = tree_element.element_type

        if tree_element.value == "identifier":
            self.class_name = tree_element.child_value
            if parent.classVarDec:
                for class_var_dec in parent.classVarDec:
                    self.handle_class_var_dec(class_var_dec)

        if element_value == "statements":
            self.handle_statements(tree_element)

        if element_value == "subroutineDec":
            self.symbol_table.start_subroutine()
            self.handle_subroutineDec(tree_element)

        if tree_element.is_leaf:

            if element_type == "identifier":
                # 클래스 이름 가져오기
                if tree_element.identifier_category() == IdentifierCategory.CLASS:
                    if parent.parent.classVarDec:
                        for class_var_dec in parent.parent.classVarDec:
                            self.handle_class_var_dec(class_var_dec)

            return

    def handle_parameter_list(self, parameter_list_element: TreeElement) -> None:
        element_strs: List[str] = list(
            filter(
                lambda x: x.element_type in ["keyword", "identifier"],
                parameter_list_element.post_traverse(),
            )
        )

        for idx in range(0, len(element_strs), 2):
            param_type = element_strs[idx].value
            param_name = element_strs[idx + 1].value
            self.symbol_table.define(param_name, param_type, SymbolKind.ARG)

    def handle_var_dec(self, var_dec_element: TreeElement) -> int:
        if var_dec_element.visited:
            return
        var_dec_element.visited = True

        var_type: Optional[str] = None
        vars: List[str] = []
        for idx, element in enumerate(var_dec_element.post_traverse()):
            if idx == 1:
                var_type = element.value
            elif element.element_type == "identifier":
                vars.append(element.value)

        if not var_type:
            raise RuntimeError("Unable to parse type of declared variables.")

        for var in vars:
            self.symbol_table.define(var, var_type, SymbolKind.VAR)
        return len(vars)

    def handle_class_var_dec(self, class_var_dec: TreeElement) -> None:
        element_strs: List[str] = list(
            filter(
                lambda x: x.element_type in ["keyword", "identifier"],
                class_var_dec.post_traverse(),
            )
        )

        symbol_type = element_strs[0].value
        param_type = element_strs[1].value

        for element in element_strs[2:]:
            param_name = element.value
            if symbol_type == "field":
                self.symbol_table.define(param_name, param_type, SymbolKind.FIELD)
                self.class_var_dec_count += 1
            elif symbol_type == "static":
                self.symbol_table.define(param_name, param_type, SymbolKind.STATIC)

    def handle_statements(self, statements: TreeElement) -> None:
        statements.visited = True
        if statements.value is not "statements":
            return

        for tree_element in statements.children:
            if tree_element.value == "doStatement":
                self.handle_do_statement(tree_element)

            if tree_element.value == "letStatement":
                self.handle_let_statement(tree_element)
            if tree_element.value == "returnStatement":
                self.handle_return_statement(tree_element)
            if tree_element.value == "whileStatement":
                self.handle_while_statement(tree_element)
            if tree_element.value == "ifStatement":
                self.handle_if_statement(tree_element)

    def handle_subroutineDec(self, tree_element: TreeElement) -> None:
        if tree_element.visited:
            return
        tree_element.visited = True

        subroutine_type: Optional[SubroutineTypeEnum] = None
        subroutine_name: str = ""

        if tree_element.keyword[0]:
            match tree_element.keyword[0].child_value:
                case "function":
                    subroutine_type = SubroutineTypeEnum.FUNC
                case "method":
                    subroutine_type = SubroutineTypeEnum.METHOD
                case "constructor":
                    subroutine_type = SubroutineTypeEnum.CONSTRUCTOR

        # Determine subroutine name
        for sub_element in tree_element.post_traverse():
            if sub_element.element_type == "symbol" and sub_element.value == "(":
                break
            elif sub_element.element_type == "identifier":
                subroutine_name = sub_element.value

        if subroutine_type == SubroutineTypeEnum.METHOD:
            self.symbol_table.define("this", self.class_name, SymbolKind.ARG)
        self.handle_parameter_list(tree_element.parameterList[0])

        var_decs = tree_element.subroutineBody[0].varDec
        var_dec_count: int = 0
        if var_decs is not None:
            for var_dec in var_decs:
                var_dec_count += self.handle_var_dec(var_dec)

        self.vm_writer.write_function(
            f"{self.class_name}.{subroutine_name}", var_dec_count
        )
        if not subroutine_type:
            raise RuntimeError("Unable to determine subroutine type.")
        if subroutine_type == SubroutineTypeEnum.CONSTRUCTOR:
            # Note) static을 제외한 필드만 처리하도록 해야함
            self.vm_writer.write_push(SegmentEnum.CONST, self.class_var_dec_count)
            self.vm_writer.write_call("Memory.alloc", 1)
        if subroutine_type == SubroutineTypeEnum.METHOD:
            self.vm_writer.write_push(SegmentEnum.ARG, 0)
        if subroutine_type in [
            SubroutineTypeEnum.METHOD,
            SubroutineTypeEnum.CONSTRUCTOR,
        ]:
            self.vm_writer.write_pop(SegmentEnum.POINTER, 0)

        for statements in tree_element.subroutineBody[0].statements:
            self.handle_statements(statements)

    def handle_do_statement(self, tree_element: TreeElement) -> None:
        if tree_element.visited:
            return
        tree_element.visited = True

        expression_list = tree_element.expressionList[0]
        symbols = [x.child_value for x in tree_element.symbol]

        subroutine_type: CalledSubroutineTypeEnum = CalledSubroutineTypeEnum.FUNC
        if "." not in symbols:
            # calls subroutine method which is in same class
            subroutine_type = CalledSubroutineTypeEnum.SAME_CLASS_METHOD
        else:
            subroutine_type = (
                CalledSubroutineTypeEnum.METHOD
                if self.symbol_table.index_of(tree_element.identifier[0].child_value)
                is not None
                else CalledSubroutineTypeEnum.FUNC
            )

        method_class = self.symbol_table.type_of(tree_element.identifier[0].child_value)
        subroutine_name = ""
        if subroutine_type in [
            CalledSubroutineTypeEnum.METHOD,
            CalledSubroutineTypeEnum.SAME_CLASS_METHOD,
        ]:
            # check if subroutine is same class's method => ex) do erase()
            if "." in symbols:
                subroutine_name = ".".join(
                    [method_class, tree_element.identifier[1].child_value]
                )
            else:
                subroutine_name = ".".join(
                    [self.class_name, tree_element.identifier[0].child_value]
                )
        else:
            subroutine_name = ".".join(
                map(lambda x: x.child_value, tree_element.identifier)
            )
        subroutine_arg_count = (
            len(expression_list.expression) if expression_list.expression else 0
        )

        if subroutine_type in [
            CalledSubroutineTypeEnum.METHOD,
            CalledSubroutineTypeEnum.SAME_CLASS_METHOD,
        ]:
            if subroutine_type == CalledSubroutineTypeEnum.SAME_CLASS_METHOD:
                self.vm_writer.write_push(SegmentEnum.POINTER, 0)
            subroutine_arg_count += 1
            symbol_kind = self.symbol_table.kind_of(
                tree_element.identifier[0].child_value
            )
            symbol_index = self.symbol_table.index_of(
                tree_element.identifier[0].child_value
            )
            if symbol_kind == SymbolKind.ARG:
                self.vm_writer.write_push(SegmentEnum.ARG, symbol_index)
            elif symbol_kind == SymbolKind.FIELD:
                self.vm_writer.write_push(SegmentEnum.THIS, symbol_index)
            elif symbol_kind == SymbolKind.STATIC:
                self.vm_writer.write_push(SegmentEnum.STATIC, symbol_index)
            elif symbol_kind == SymbolKind.VAR:
                self.vm_writer.write_push(SegmentEnum.LOCAL, symbol_index)

        if expression_list.expression:
            for expression in expression_list.expression:
                self.handle_expression_element(expression)

        self.vm_writer.write_call(subroutine_name, subroutine_arg_count)
        self.vm_writer.write_pop(SegmentEnum.TEMP, 0)

    def handle_if_statement(self, tree_element: TreeElement) -> None:
        if tree_element.visited:
            return
        tree_element.visited = True

        self.label_count += 2
        current_label_count = self.label_count

        has_else_statement: bool = True if len(tree_element.statements) > 1 else False

        self.handle_expression_element(tree_element.expression[0])
        self.vm_writer.write_arithmetic(ArithCommandEnum.NOT)
        if has_else_statement:
            self.vm_writer.write_if(f"label{current_label_count-1}")
        else:
            self.vm_writer.write_if(f"label{current_label_count}")
        self.handle_statements(tree_element.statements[0])
        self.vm_writer.write_goto(f"label{current_label_count}")

        if has_else_statement:
            self.vm_writer.write_label(f"label{current_label_count-1}")
            self.handle_statements(tree_element.statements[1])
        self.vm_writer.write_label(f"label{current_label_count}")

    def handle_while_statement(self, tree_element: TreeElement) -> None:
        self.label_count += 2
        current_label_count = self.label_count

        if tree_element.visited:
            return
        tree_element.visited = True

        self.vm_writer.write_label(f"label{current_label_count-1}")
        self.handle_expression_element(tree_element.expression[0])
        self.vm_writer.write_arithmetic(ArithCommandEnum.NOT)
        self.vm_writer.write_if(f"label{current_label_count}")

        self.handle_statements(tree_element.statements[0])

        self.vm_writer.write_goto(f"label{current_label_count-1}")
        self.vm_writer.write_label(f"label{current_label_count}")

    def handle_let_statement(self, tree_element: TreeElement) -> None:
        if tree_element.visited:
            return
        tree_element.visited = True
        var_name = tree_element.identifier[0].child_value
        var_symbol_index = self.symbol_table.index_of(var_name)
        var_symbol_kind = self.symbol_table.kind_of(var_name)
        is_var_array: bool = False
        symbols: List[str] = map(lambda x: x.child_value, tree_element.symbol)

        if var_symbol_index is None:
            raise RuntimeError("Undefined symbol used in let statement.")

        if "[" in symbols and "]" in symbols:
            is_var_array = True

        if is_var_array:
            if var_symbol_kind == SymbolKind.VAR:
                self.vm_writer.write_push(SegmentEnum.LOCAL, var_symbol_index)
            elif var_symbol_kind == SymbolKind.ARG:
                self.vm_writer.write_push(SegmentEnum.ARG, var_symbol_index)
            elif var_symbol_kind == SymbolKind.FIELD:
                self.vm_writer.write_push(SegmentEnum.THIS, var_symbol_index)
            elif var_symbol_kind == SymbolKind.STATIC:
                self.vm_writer.write_push(SegmentEnum.STATIC, var_symbol_index)

        for idx, expression in enumerate(tree_element.expression):
            if idx == 1 and is_var_array:
                # handle [ expression ]
                self.vm_writer.write_arithmetic(ArithCommandEnum.ADD)
            self.handle_expression_element(expression)

        if is_var_array:
            # save xpression resut to temp 1
            self.vm_writer.write_pop(SegmentEnum.TEMP, 0)
            self.vm_writer.write_pop(SegmentEnum.POINTER, 1)
            self.vm_writer.write_push(SegmentEnum.TEMP, 0)
            self.vm_writer.write_pop(SegmentEnum.THAT, 0)
        else:
            if var_symbol_index is None or var_symbol_kind is None:
                raise RuntimeError("Undefined symbol used.")
            if var_symbol_kind == SymbolKind.VAR:
                self.vm_writer.write_pop(SegmentEnum.LOCAL, var_symbol_index)
            elif var_symbol_kind == SymbolKind.ARG:
                self.vm_writer.write_pop(SegmentEnum.ARG, var_symbol_index)
            elif var_symbol_kind == SymbolKind.FIELD:
                self.vm_writer.write_pop(SegmentEnum.THIS, var_symbol_index)
            elif var_symbol_kind == SymbolKind.STATIC:
                self.vm_writer.write_pop(SegmentEnum.STATIC, var_symbol_index)

    def handle_expression_element(self, expression_element: TreeElement) -> None:
        if expression_element.visited:
            return
        expression_element.visited = True

        arithmetic_op: Optional[str] = None

        for child in expression_element.children:
            if child.value == "term":
                self.handle_term_element(child)
                if arithmetic_op:
                    self.handle_arithmetic_op(arithmetic_op)
            elif child.value == "symbol" and child.child_value in [
                "-",
                "+",
                "*",
                "/",
                "~",
                "<",
                ">",
                "=",
                "&",
                "|",
            ]:
                arithmetic_op = child.child_value

        if (
            expression_element.term[0].expressionList
            and expression_element.term[0].expressionList[0].expression
        ):
            for sub_expression in (
                expression_element.term[0].expressionList[0].expression
            ):
                self.handle_expression_element(sub_expression)

    def handle_term_element(self, term_element: TreeElement) -> None:
        has_sub_expression: bool = (
            True
            if term_element.expressionList is not None
            or term_element.expression is not None
            or term_element.term is not None
            else False
        )
        arithmetic_op: Optional[str] = None

        sub_elements = term_element.post_traverse()

        is_var_array: bool = False
        symbols: List[str] = []

        if term_element.symbol:
            symbols = map(lambda x: x.child_value, term_element.symbol)
        if "[" in symbols and "]" in symbols:
            is_var_array = True

        if is_var_array:
            var_name = term_element.identifier[0].child_value
            symbol_kind = self.symbol_table.kind_of(var_name)
            symbol_index = self.symbol_table.index_of(var_name)
            if symbol_index is None or symbol_kind is None:
                raise RuntimeError("Undefined symbol used.")
            elif symbol_kind == SymbolKind.VAR:
                self.vm_writer.write_push(SegmentEnum.LOCAL, symbol_index)
            elif symbol_kind == SymbolKind.ARG:
                self.vm_writer.write_push(SegmentEnum.ARG, symbol_index)
            elif symbol_kind == SymbolKind.FIELD:
                self.vm_writer.write_push(SegmentEnum.THIS, symbol_index)
            elif symbol_kind == SymbolKind.STATIC:
                self.vm_writer.write_push(SegmentEnum.STATIC, symbol_index)

        if not has_sub_expression:
            # 하위 expression이 없으면 실질적인 처리를 한다.
            for sub_element in sub_elements:
                value = sub_element.value
                type = sub_element.element_type

                if type == "symbol" and value == "]":
                    if is_var_array:
                        self.vm_writer.write_arithmetic(ArithCommandEnum.ADD)
                if type == "integerConstant":
                    self.vm_writer.write_push(SegmentEnum.CONST, int(value))
                if type == "stringConstant":
                    # calculate string length
                    self.vm_writer.write_push(SegmentEnum.CONST, len(value))
                    self.vm_writer.write_call("String.new", 1)
                    for ch in value:
                        self.vm_writer.write_push(SegmentEnum.CONST, ord(ch))
                        self.vm_writer.write_call("String.appendChar", 2)
                if type == "keyword":
                    match value:
                        case "true":
                            self.vm_writer.write_push(SegmentEnum.CONST, 1)
                            self.vm_writer.write_arithmetic(ArithCommandEnum.NEG)
                        case "false":
                            self.vm_writer.write_push(SegmentEnum.CONST, 0)
                        case "null":
                            self.vm_writer.write_push(SegmentEnum.CONST, 0)
                        case "this":
                            self.vm_writer.write_push(SegmentEnum.POINTER, 0)
                if type == "identifier":
                    symbol_index = self.symbol_table.index_of(value)
                    symbol_kind = self.symbol_table.kind_of(value)
                    if symbol_index is None or symbol_kind is None:
                        raise RuntimeError("Undefined symbol used.")
                    if symbol_kind == SymbolKind.VAR:
                        self.vm_writer.write_push(SegmentEnum.LOCAL, symbol_index)
                    elif symbol_kind == SymbolKind.ARG:
                        self.vm_writer.write_push(SegmentEnum.ARG, symbol_index)
                    elif symbol_kind == SymbolKind.FIELD:
                        self.vm_writer.write_push(SegmentEnum.THIS, symbol_index)
                    elif symbol_kind == SymbolKind.STATIC:
                        self.vm_writer.write_push(SegmentEnum.STATIC, symbol_index)

        else:
            if term_element.expressionList:
                for expression in filter(
                    lambda x: x.value == "expression",
                    term_element.expressionList[0].children,
                ):
                    self.handle_expression_element(expression)
            if term_element.expression:
                for expression in term_element.expression:
                    self.handle_expression_element(expression)
            if term_element.term:
                for sub_term_element in term_element.term:
                    self.handle_term_element(sub_term_element)

        if is_var_array:
            self.vm_writer.write_arithmetic(ArithCommandEnum.ADD)
            self.vm_writer.write_pop(SegmentEnum.POINTER, 1)  # pop pointer 1
            self.vm_writer.write_push(SegmentEnum.THAT, 0)  # pop that 0

        # check if subroutine is called or not
        is_subroutine_call = False
        symbol_elements = term_element.symbol
        if symbol_elements:
            symbols: List[str] = list(map(lambda x: x.child_value, symbol_elements))
            if "(" in symbols and ")" in symbols and symbols.index("(") != 0:
                is_subroutine_call = True
            for symbol_element in symbol_elements:
                if symbol_element.child_value in ["-", "~", "<", ">"]:
                    arithmetic_op = symbol_element.child_value

        if is_subroutine_call:
            subroutine_names: List[str] = []
            for sub_element in term_element.post_traverse():
                if sub_element.element_type == "symbol" and sub_element.value == "(":
                    break
                if sub_element.element_type == "identifier":
                    subroutine_names.append(sub_element.value)

            is_subrountine_method = (
                True
                if self.symbol_table.index_of(subroutine_names[0]) is not None
                else False
            )
            method_class = self.symbol_table.type_of(subroutine_names[0])

            subroutine_name = ""
            if is_subrountine_method:
                subroutine_name = ".".join([method_class, subroutine_names[1]])
            else:
                subroutine_name = ".".join(subroutine_names)
            arg_expressions = term_element.expressionList[0].expression

            arg_count = len(arg_expressions) if arg_expressions is not None else 0
            if is_subrountine_method:
                arg_count += 1
                symbol_kind = self.symbol_table.kind_of(subroutine_names[0])
                symbol_index = self.symbol_table.index_of(subroutine_names[0])
                # TODO : Add exception handling
                if symbol_kind == SymbolKind.ARG:
                    self.vm_writer.write_push(SegmentEnum.ARG, symbol_index)
                elif symbol_kind == SymbolKind.FIELD:
                    self.vm_writer.write_push(SegmentEnum.THIS, symbol_index)
                elif symbol_kind == SymbolKind.STATIC:
                    self.vm_writer.write_push(SegmentEnum.STATIC, symbol_index)
                elif symbol_kind == SymbolKind.VAR:
                    self.vm_writer.write_push(SegmentEnum.LOCAL, symbol_index)
            self.vm_writer.write_call(subroutine_name, arg_count)

        if arithmetic_op:
            match arithmetic_op:
                case "-":
                    self.vm_writer.write_arithmetic(ArithCommandEnum.NEG)
                case "~":
                    self.vm_writer.write_arithmetic(ArithCommandEnum.NOT)

    def handle_return_statement(self, tree_element: TreeElement) -> None:
        has_expression: bool = True if tree_element.expression is not None else False

        if has_expression:
            self.handle_expression_element(tree_element.expression[0])
            self.vm_writer.write_return()
        else:
            self.vm_writer.write_push(SegmentEnum.CONST, 0)
            self.vm_writer.write_return()

    def handle_arithmetic_op(self, arithmetic_op: str) -> None:
        match arithmetic_op:
            case "+":
                self.vm_writer.write_arithmetic(ArithCommandEnum.ADD)
            case "-":
                self.vm_writer.write_arithmetic(ArithCommandEnum.SUB)
            case "*":
                self.vm_writer.write_call("Math.multiply", 2)
            case "/":
                self.vm_writer.write_call("Math.divide", 2)
            case "~":
                self.vm_writer.write_arithmetic(ArithCommandEnum.NOT)
            case "<":
                self.vm_writer.write_arithmetic(ArithCommandEnum.LT)
            case ">":
                self.vm_writer.write_arithmetic(ArithCommandEnum.GT)
            case "=":
                self.vm_writer.write_arithmetic(ArithCommandEnum.EQ)
            case "&":
                self.vm_writer.write_arithmetic(ArithCommandEnum.AND)
            case "|":
                self.vm_writer.write_arithmetic(ArithCommandEnum.OR)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Missing required argument. Pass path to compile.")
    target_path = pathlib.Path(sys.argv[1])

    jack_compiler = JackCompiler(mode=JackCompilerModeEnum.COMPILE)
    jack_compiler.target_path = target_path
    jack_compiler.analyze_token()
    jack_compiler.compile()
