from enum import Enum
from typing import Callable, List, Optional

from compiler.rule import (
    ListRuleElement,
    MultipleRuleElement,
    OrRuleElement,
    RefRuleElement,
    RuleElement,
    RuleElementType,
    RuleError,
    ZeroOneRuleElement,
)
from compiler.rule_definition import (
    KEYWORD_CONSTANT_RULE_ELEMENTS,
    OP_RULE_ELEMENTS,
    TYPE_RULE_ELEMENTS,
    UNARY_OP_RULE_ELEMENTS,
)
from compiler.tokenizer import Token, Tokenizer, TokenType


class IdentifierCategory(Enum):
    VAR = 0
    ARG = 1
    STATIC = 2
    FIELD = 3
    CLASS = 4
    SUBROUTINE = 5


class IdentifierUsageType(Enum):
    STATEMENT = 0
    EXPRESSION = 1


def validate_rule_instance(rule_class: type[RuleElement]):
    def wrapper(func: Callable):
        def wrapper_func(*args, **kwargs):
            rule_element = kwargs.get("rule_element")
            if not isinstance(rule_element, rule_class):
                raise RuntimeError("Invalid rule element provided.")
            result = func(*args, **kwargs)
            return result

        return wrapper_func

    return wrapper


class TreeElement:
    def __init__(
        self,
        is_leaf: Optional[bool] = False,
        value: Optional[str] = "",
    ):
        self.is_leaf = is_leaf
        self.value = value
        self.parent: Optional[TreeElement] = None
        self.children: List["TreeElement"] = []
        self.visited: bool = False

    def set_parent(self, parent: "TreeElement") -> None:
        self.parent = parent

    def add_child(self, child: "TreeElement") -> None:
        child.set_parent(self)
        self.children.append(child)

    def extend_children(self, children: Optional[List["TreeElement"]]) -> None:
        if children is not None:
            for child in children:
                child.set_parent(self)
            self.children.extend(children)

    # access to children by tree element value
    def __getattr__(self, name):
        target_children: List[TreeElement] = []
        for child in self.children:
            if child.value == name:
                target_children.append(child)
        if len(target_children) > 0:
            return target_children
        return None

    # return value of first child
    @property
    def child_value(self) -> str:
        if len(self.children) > 0:
            return self.children[0].value
        return ""

    # if element is a leaf, assume parent element's value is a type of leaf
    # ex) keyword, identifier
    @property
    def element_type(self) -> Optional[str]:
        if self.is_leaf is False:
            return None
        return self.parent.value

    def identifier_category(self) -> IdentifierCategory:
        if self.parent is None:
            raise RuntimeError("Parent not set. Cannot identify category")

        type_element = self.parent

        if type_element.value != "identifier":
            raise RuntimeError("Not an identifier type.")

        if type_element.parent.value == "subroutineDec":
            return IdentifierCategory.SUBROUTINE

        if type_element.parent.value == "parameterList":
            return IdentifierCategory.ARG

        for neighbor in type_element.parent.children:
            if neighbor.value == "keyword":
                if neighbor.children[0].value == "field":
                    return IdentifierCategory.FIELD
                elif neighbor.children[0].value == "static":
                    return IdentifierCategory.STATIC
                elif neighbor.children[0].value == "var":
                    return IdentifierCategory.VAR
                elif neighbor.children[0].value == "class":
                    return IdentifierCategory.CLASS

        if self.parent is None:
            raise RuntimeError("Parent not set. Cannot proceed.")

        explored_result = TreeElement.explore_parent(
            self.parent, ["classVarDec", "subroutineDec", "varDec", "letStatement"]
        )
        if explored_result is False:
            return False

        identifier_element = self.parent
        for i, neighbor_element in enumerate(identifier_element.parent.children):
            if neighbor_element.children[0].value == self.value and i - 1 >= 0:
                if i == 2:
                    return True
                break

        return False

    @staticmethod
    def explore_parent(
        element: "TreeElement", target_values: List[str]
    ) -> Optional[str]:
        if element.value in target_values:
            return element.value
        if element.parent is None:
            return None
        return TreeElement.explore_parent(element.parent, target_values)

    # note: only traverse leafs
    def post_traverse(self):
        if len(self.children) == 0 and self.is_leaf:
            return [self]
        traverse_result = []
        for child in self.children:
            traverse_result.extend(child.post_traverse())
        if self.is_leaf:
            traverse_result.append(self)
        return traverse_result

    def pre_traverse(self):
        if len(self.children) == 0:
            return [self]
        traverse_result = [self]
        for child in self.children:
            traverse_result.extend(child.pre_traverse())
        return traverse_result


class Tree:
    def __init__(self):
        self.root: Optional[TreeElement] = None

    def extend_elements(self, elements: List[TreeElement]) -> None:
        self.root.extend_children(elements)

    def post_traverse(self) -> List[TreeElement]:
        result = []
        for child in self.root.children:
            result.extend(child.post_traverse())
        return result

    def pre_traverse(self) -> List[TreeElement]:
        result = []
        for child in self.root.children:
            result.extend(child.pre_traverse())
        return result


class CompileEngine:

    def __init__(self, file_path):
        self.compiled_tree: Tree = Tree()
        with open(file_path, "r") as f:
            self.tokenizer: Tokenizer = Tokenizer(f)
        self.tokenizer.tokens.append(Token(value="", type=TokenType.string_constant))

    @validate_rule_instance(rule_class=RuleElement)
    def _process_general_rule(
        self, token_type: Token, token_value: str, *, rule_element: RuleElement
    ) -> Optional[List[TreeElement]]:
        if rule_element.element_type == RuleElementType.STRING_CONSTANT:
            if token_type == TokenType.string_constant:
                self.tokenizer.advance()
                elm = TreeElement(is_leaf=False, value=token_type.value)
                elm.add_child(TreeElement(is_leaf=True, value=token_value))
                return [elm]
        elif rule_element.element_type == RuleElementType.INTEGER_CONSTANT:
            if token_type == TokenType.integer_constant:
                self.tokenizer.advance()
                elm = TreeElement(is_leaf=False, value=token_type.value)
                elm.add_child(TreeElement(is_leaf=True, value=token_value))
                return [elm]
        elif rule_element.element_type == RuleElementType.FIXED_TERMINAL:
            if token_type not in [
                TokenType.keyword,
                TokenType.symbol,
                TokenType.integer_constant,
                TokenType.string_constant,
                TokenType.identifier,
            ]:
                raise RuleError(
                    f"Token is not keyword | symbol | constant | identifier type. Parsed should be : {rule_element.desc}"
                )
            if rule_element.compare_with_token(token_value) is False:
                raise RuleError(f"Parsed should be : {rule_element.desc}")

            self.tokenizer.advance()
            elm = TreeElement(is_leaf=False, value=token_type.name)
            elm.add_child(TreeElement(is_leaf=True, value=token_value))
            return [elm]
        elif rule_element.element_type == RuleElementType.VAR_TERMINAL:
            if token_type in [TokenType.keyword, TokenType.symbol]:
                raise RuleError("Var terminal should not be keyword | symbol type.")
            self.tokenizer.advance()
            elm = TreeElement(is_leaf=False, value=token_type.name)
            elm.add_child(TreeElement(is_leaf=True, value=token_value))
            return [elm]

    @validate_rule_instance(rule_class=RefRuleElement)
    def _process_ref_rule(
        self, *, rule_element: RefRuleElement
    ) -> Optional[List[TreeElement]]:
        if isinstance(rule_element.ref, RuleElement):
            return self.process_rule_element(rule_element.ref)
        elif callable(rule_element.ref):
            r = rule_element.ref()
            if r is None:
                raise RuleError("Rule not match")
            if isinstance(r, list):
                return r
            return [r]
        raise RuleError(
            "Unexpected ref value. RefRuleElement's ref should be either RuleElement or Callable"
        )

    @validate_rule_instance(rule_class=OrRuleElement)
    def _process_or_rule(
        self, *, rule_element: OrRuleElement
    ) -> Optional[List[TreeElement]]:
        for or_elm in rule_element.or_elements:
            try:
                result = self.process_rule_element(or_elm)
                if result is not None:
                    return result
            except RuleError:
                pass

        raise RuleError("None of matched with OR rule elements")

    @validate_rule_instance(rule_class=ListRuleElement)
    def _process_list_rule(
        self, *, rule_element: ListRuleElement
    ) -> Optional[List[TreeElement]]:

        result = []
        for i, rule in enumerate(rule_element.rules):
            try:
                result.extend(self.process_rule_element(rule))
            except RuleError as e:
                self.tokenizer.previous(i)
                raise RuleError(e.msg)
        return result

    @validate_rule_instance(rule_class=MultipleRuleElement)
    def _process_multiple_rule(
        self, *, rule_element: MultipleRuleElement
    ) -> Optional[List[TreeElement]]:

        results = []
        while True:
            try:
                if isinstance(rule_element.ref, RuleElement):
                    a = self.process_rule_element(rule_element.ref)
                elif callable(rule_element.ref):
                    a = rule_element.ref()
                else:
                    raise RuleError(
                        "Unexpected ref value. MultipleRuleElement's ref should be either RuleElement "
                        "or Callable"
                    )
                if a is not None and isinstance(a, list):
                    results.extend(a)
                elif a is not None:
                    results.append(a)
            except RuleError:
                break

        return results

    @validate_rule_instance(rule_class=ZeroOneRuleElement)
    def _process_zero_one_rule(
        self, *, rule_element: ZeroOneRuleElement
    ) -> Optional[List[TreeElement]]:
        # 없거나 한개
        results = []
        try:
            if isinstance(rule_element.ref, RuleElement):
                a = self.process_rule_element(rule_element.ref)
            elif callable(rule_element.ref):
                a = rule_element.ref()
            else:
                raise RuleError(
                    "Unexpected ref value. MultipleRuleElement's ref should be either RuleElement "
                    "or Callable"
                )
            if a is None:
                return
            elif a is not None and isinstance(a, list):
                results.extend(a)
            elif a is not None:
                results.append(a)
            return results
        except RuleError:
            return

    def process_rule_element(
        self, rule_element: RuleElement
    ) -> Optional[List[TreeElement]]:
        token_type = self.tokenizer.token_type()
        token_value = self.tokenizer.current_token.value

        if rule_element.element_type in [
            RuleElementType.STRING_CONSTANT,
            RuleElementType.INTEGER_CONSTANT,
            RuleElementType.FIXED_TERMINAL,
            RuleElementType.VAR_TERMINAL,
        ]:
            return self._process_general_rule(
                token_type, token_value, rule_element=rule_element
            )
        elif rule_element.element_type == RuleElementType.REF:
            return self._process_ref_rule(rule_element=rule_element)
        elif rule_element.element_type == RuleElementType.OR:
            return self._process_or_rule(rule_element=rule_element)
        elif rule_element.element_type == RuleElementType.LIST:
            return self._process_list_rule(rule_element=rule_element)
        elif rule_element.element_type == RuleElementType.MULTIPLE:
            return self._process_multiple_rule(rule_element=rule_element)
        elif rule_element.element_type == RuleElementType.ZERO_OR_ONE:
            return self._process_zero_one_rule(rule_element=rule_element)

    def start_compile(self):
        if self.tokenizer.has_more_token() is False:
            raise RuntimeError("no more token to process")
        self.tokenizer.advance()
        # always call compile_class first.
        self.compile_class()

    def _compile_subroutine_call(self) -> List[TreeElement]:
        rule = RefRuleElement(
            desc="subroutineCall",
            ref=OrRuleElement(
                desc="subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'",
                or_elements=[
                    ListRuleElement(
                        desc="subroutineName '(' expressionList ')'",
                        rules=[
                            RuleElement(RuleElementType.VAR_TERMINAL, "subroutineName"),
                            RuleElement(RuleElementType.FIXED_TERMINAL, "("),
                            RefRuleElement(
                                desc="expressionList", ref=self.compile_expression_list
                            ),
                            RuleElement(RuleElementType.FIXED_TERMINAL, ")"),
                        ],
                    ),
                    ListRuleElement(
                        desc="(className | varName) '.' subroutineName '(' expressionList ')'",
                        rules=[
                            OrRuleElement(
                                desc="(className | varName)",
                                or_elements=[
                                    RuleElement(
                                        RuleElementType.VAR_TERMINAL, "className"
                                    ),
                                    RuleElement(
                                        RuleElementType.VAR_TERMINAL, "varName"
                                    ),
                                ],
                            ),
                            RuleElement(RuleElementType.FIXED_TERMINAL, "."),
                            RuleElement(RuleElementType.VAR_TERMINAL, "subroutineName"),
                            RuleElement(RuleElementType.FIXED_TERMINAL, "("),
                            RefRuleElement(
                                desc="expressionList", ref=self.compile_expression_list
                            ),
                            RuleElement(RuleElementType.FIXED_TERMINAL, ")"),
                        ],
                    ),
                ],
            ),
        )

        r = self.process_rule_element(rule)
        return r

    def compile_class(self):
        self.compiled_tree.root = TreeElement(value="class", is_leaf=False)
        class_rules: List[RuleElement] = [
            RuleElement(RuleElementType.FIXED_TERMINAL, "class"),
            RuleElement(RuleElementType.VAR_TERMINAL, "className"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "{"),
            MultipleRuleElement(desc="classVarDec*", ref=self.compile_class_var_dec),
            MultipleRuleElement(desc="subroutineDec*", ref=self.compile_subroutine),
            RuleElement(RuleElementType.FIXED_TERMINAL, "}"),
        ]

        for rule in class_rules:
            self.compiled_tree.extend_elements(self.process_rule_element(rule))

    def compile_class_var_dec(self) -> Optional[TreeElement]:
        tree_element = TreeElement(value="classVarDec", is_leaf=False)
        rules: List[RuleElement] = [
            OrRuleElement(
                desc="'static' | 'field'",
                or_elements=[
                    RuleElement(RuleElementType.FIXED_TERMINAL, "static"),
                    RuleElement(RuleElementType.FIXED_TERMINAL, "field"),
                ],
            ),
            OP_RULE_ELEMENTS,
            RuleElement(RuleElementType.VAR_TERMINAL, "varName"),
            MultipleRuleElement(
                desc="(',' varName)*",
                ref=ListRuleElement(
                    desc="(',' varName)",
                    rules=[
                        RuleElement(RuleElementType.FIXED_TERMINAL, ","),
                        RuleElement(RuleElementType.VAR_TERMINAL, "varName"),
                    ],
                ),
            ),
            RuleElement(RuleElementType.FIXED_TERMINAL, ";"),
        ]
        for rule in rules:
            tree_element.extend_children(self.process_rule_element(rule))
        return tree_element

    def compile_subroutine(self):
        tree_element = TreeElement(value="subroutineDec", is_leaf=False)
        rules: List[RuleElement] = [
            OrRuleElement(
                desc="'constructor' | 'function' | 'method'",
                or_elements=[
                    RuleElement(RuleElementType.FIXED_TERMINAL, "constructor"),
                    RuleElement(RuleElementType.FIXED_TERMINAL, "function"),
                    RuleElement(RuleElementType.FIXED_TERMINAL, "method"),
                ],
            ),
            OrRuleElement(
                desc="'void' | type ",
                or_elements=[
                    RuleElement(RuleElementType.FIXED_TERMINAL, "void"),
                    TYPE_RULE_ELEMENTS,
                ],
            ),
            RuleElement(RuleElementType.VAR_TERMINAL, "subroutineName"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "("),
            RefRuleElement(desc="parameterList", ref=self.compile_parameter_list),
            RuleElement(RuleElementType.FIXED_TERMINAL, ")"),
            RefRuleElement(desc="subroutineBody", ref=self.compile_subroutine_body),
        ]
        for rule in rules:
            tree_element.extend_children(self.process_rule_element(rule))
        return tree_element

    def compile_parameter_list(self):
        tree_element = TreeElement(value="parameterList", is_leaf=False)
        rules: List[RuleElement] = [
            ZeroOneRuleElement(
                desc="((type varName) (',' type varName)*)?",
                ref=ListRuleElement(
                    desc="(type varName) (',' type varName)*",
                    rules=[
                        ListRuleElement(
                            desc="(type varName)",
                            rules=[
                                TYPE_RULE_ELEMENTS,
                                RuleElement(RuleElementType.VAR_TERMINAL, "varName"),
                            ],
                        ),
                        MultipleRuleElement(
                            desc="(',' type varName)*",
                            ref=ListRuleElement(
                                desc="',' type varName",
                                rules=[
                                    RuleElement(RuleElementType.FIXED_TERMINAL, ","),
                                    TYPE_RULE_ELEMENTS,
                                    RuleElement(
                                        RuleElementType.VAR_TERMINAL, "varName"
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            )
        ]
        for rule in rules:
            tree_element.extend_children(self.process_rule_element(rule))
        return tree_element

    def compile_subroutine_body(self):
        tree_element = TreeElement(value="subroutineBody", is_leaf=False)
        rules: List[RuleElement] = [
            RuleElement(RuleElementType.FIXED_TERMINAL, "{"),
            MultipleRuleElement(desc="varDec*", ref=self.compile_var_dec),
            RefRuleElement(desc="statements", ref=self.compile_statements),
            RuleElement(RuleElementType.FIXED_TERMINAL, "}"),
        ]
        for rule in rules:
            tree_element.extend_children(self.process_rule_element(rule))
        return tree_element

    def compile_var_dec(self):
        tree_element = TreeElement(value="varDec", is_leaf=False)
        rules: List[RuleElement] = [
            RuleElement(RuleElementType.FIXED_TERMINAL, "var"),
            TYPE_RULE_ELEMENTS,
            RuleElement(RuleElementType.VAR_TERMINAL, "varName"),
            MultipleRuleElement(
                desc="(',' varName)*",
                ref=ListRuleElement(
                    desc="(',' varName)",
                    rules=[
                        RuleElement(RuleElementType.FIXED_TERMINAL, ","),
                        RuleElement(RuleElementType.VAR_TERMINAL, "varName"),
                    ],
                ),
            ),
            RuleElement(RuleElementType.FIXED_TERMINAL, ";"),
        ]
        for rule in rules:
            tree_element.extend_children(self.process_rule_element(rule))
        return tree_element

    def compile_statements(self):
        tree_element = TreeElement(value="statements", is_leaf=False)
        rules: List[RuleElement] = [
            MultipleRuleElement(
                desc="statement*",
                ref=OrRuleElement(
                    desc="'letStatement' | 'ifStatement' | 'whileStatement' | 'doStatement' | 'returnStatement'",
                    or_elements=[
                        RefRuleElement(desc="letStatement", ref=self.compile_let),
                        RefRuleElement(desc="ifStatement", ref=self.compile_if),
                        RefRuleElement(desc="whileStatement", ref=self.compile_while),
                        RefRuleElement(desc="doStatement", ref=self.compile_do),
                        RefRuleElement(desc="returnStatement", ref=self.compile_return),
                    ],
                ),
            ),
        ]
        for rule in rules:
            tree_element.extend_children(self.process_rule_element(rule))
        return tree_element

    def compile_do(self):
        tree_element = TreeElement(value="doStatement", is_leaf=False)
        rules: List[RuleElement] = [
            RuleElement(RuleElementType.FIXED_TERMINAL, "do"),
            RefRuleElement(desc="subroutineCall", ref=self._compile_subroutine_call),
            RuleElement(RuleElementType.FIXED_TERMINAL, ";"),
        ]
        for rule in rules:
            tree_element.extend_children(self.process_rule_element(rule))
        return tree_element

    def compile_let(self):
        tree_element = TreeElement(value="letStatement", is_leaf=False)
        rules: List[RuleElement] = [
            RuleElement(RuleElementType.FIXED_TERMINAL, "let"),
            RuleElement(RuleElementType.VAR_TERMINAL, "varName"),
            ZeroOneRuleElement(
                desc="('[' expression ']')?",
                ref=ListRuleElement(
                    desc="'[' expression ']'",
                    rules=[
                        RuleElement(RuleElementType.FIXED_TERMINAL, "["),
                        RefRuleElement(desc="expression", ref=self.compile_expression),
                        RuleElement(RuleElementType.FIXED_TERMINAL, "]"),
                    ],
                ),
            ),
            RuleElement(RuleElementType.FIXED_TERMINAL, "="),
            RefRuleElement(desc="expression", ref=self.compile_expression),
            RuleElement(RuleElementType.FIXED_TERMINAL, ";"),
        ]
        for rule in rules:
            tree_element.extend_children(self.process_rule_element(rule))
        return tree_element

    def compile_while(self):
        tree_element = TreeElement(value="whileStatement", is_leaf=False)
        rules: List[RuleElement] = [
            RuleElement(RuleElementType.FIXED_TERMINAL, "while"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "("),
            RefRuleElement(desc="expression", ref=self.compile_expression),
            RuleElement(RuleElementType.FIXED_TERMINAL, ")"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "{"),
            RefRuleElement(desc="statements", ref=self.compile_statements),
            RuleElement(RuleElementType.FIXED_TERMINAL, "}"),
        ]
        for rule in rules:
            tree_element.extend_children(self.process_rule_element(rule))
        return tree_element

    def compile_return(self):
        tree_element = TreeElement(value="returnStatement", is_leaf=False)
        rules: List[RuleElement] = [
            RuleElement(RuleElementType.FIXED_TERMINAL, "return"),
            ZeroOneRuleElement(
                desc="expression?",
                ref=RefRuleElement(desc="expression", ref=self.compile_expression),
            ),
            RuleElement(RuleElementType.FIXED_TERMINAL, ";"),
        ]
        for rule in rules:
            tree_element.extend_children(self.process_rule_element(rule))
        return tree_element

    def compile_if(self):
        tree_element = TreeElement(value="ifStatement", is_leaf=False)
        rules: List[RuleElement] = [
            RuleElement(RuleElementType.FIXED_TERMINAL, "if"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "("),
            RefRuleElement(desc="expression", ref=self.compile_expression),
            RuleElement(RuleElementType.FIXED_TERMINAL, ")"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "{"),
            RefRuleElement(desc="statements", ref=self.compile_statements),
            RuleElement(RuleElementType.FIXED_TERMINAL, "}"),
            ZeroOneRuleElement(
                desc="('else' '{' statements '}')?",
                ref=ListRuleElement(
                    desc="'else' '{' statements '}'",
                    rules=[
                        RuleElement(RuleElementType.FIXED_TERMINAL, "else"),
                        RuleElement(RuleElementType.FIXED_TERMINAL, "{"),
                        RefRuleElement(desc="statements", ref=self.compile_statements),
                        RuleElement(RuleElementType.FIXED_TERMINAL, "}"),
                    ],
                ),
            ),
        ]
        for rule in rules:
            tree_element.extend_children(self.process_rule_element(rule))
        return tree_element

    def compile_expression(self):
        tree_element = TreeElement(value="expression", is_leaf=False)
        rules: List[RuleElement] = [
            RefRuleElement(desc="term", ref=self.compile_term),
            MultipleRuleElement(
                desc="(op term)*",
                ref=ListRuleElement(
                    desc="op term",
                    rules=[
                        OP_RULE_ELEMENTS,
                        RefRuleElement(desc="term", ref=self.compile_term),
                    ],
                ),
            ),
        ]
        for rule in rules:
            tree_element.extend_children(self.process_rule_element(rule))
        return tree_element

    def compile_term(self):
        tree_element = TreeElement(value="term", is_leaf=False)
        rules: List[RuleElement] = [
            OrRuleElement(
                desc="integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term",
                or_elements=[
                    RuleElement(RuleElementType.INTEGER_CONSTANT, "integerConstant"),
                    RuleElement(RuleElementType.STRING_CONSTANT, "stringConstant"),
                    KEYWORD_CONSTANT_RULE_ELEMENTS,
                    RefRuleElement(
                        desc="subroutineCall", ref=self._compile_subroutine_call
                    ),
                    ListRuleElement(
                        desc="varName '[' expression ']'",
                        rules=[
                            RuleElement(RuleElementType.VAR_TERMINAL, "varName"),
                            RuleElement(RuleElementType.FIXED_TERMINAL, "["),
                            RefRuleElement(
                                desc="expression", ref=self.compile_expression
                            ),
                            RuleElement(RuleElementType.FIXED_TERMINAL, "]"),
                        ],
                    ),
                    RuleElement(RuleElementType.VAR_TERMINAL, "varName"),
                    ListRuleElement(
                        desc="'(' expression ')'",
                        rules=[
                            RuleElement(RuleElementType.FIXED_TERMINAL, "("),
                            RefRuleElement(
                                desc="expression", ref=self.compile_expression
                            ),
                            RuleElement(RuleElementType.FIXED_TERMINAL, ")"),
                        ],
                    ),
                    ListRuleElement(
                        desc="unaryOp term",
                        rules=[
                            UNARY_OP_RULE_ELEMENTS,
                            RefRuleElement(desc="term", ref=self.compile_term),
                        ],
                    ),
                ],
            )
        ]

        for rule in rules:
            tree_element.extend_children(self.process_rule_element(rule))
        return tree_element

    def compile_expression_list(self):
        tree_element = TreeElement(value="expressionList", is_leaf=False)
        rules: List[RuleElement] = [
            ZeroOneRuleElement(
                desc="(expression, (',' expression)*)?",
                ref=ListRuleElement(
                    desc="expression, (',' expression)*",
                    rules=[
                        RefRuleElement(desc="expression", ref=self.compile_expression),
                        MultipleRuleElement(
                            desc="(',' expression)*",
                            ref=ListRuleElement(
                                desc="',' expression",
                                rules=[
                                    RuleElement(RuleElementType.FIXED_TERMINAL, ","),
                                    RefRuleElement(
                                        desc="expression", ref=self.compile_expression
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            )
        ]

        for rule in rules:
            tree_element.extend_children(self.process_rule_element(rule))
        return tree_element
