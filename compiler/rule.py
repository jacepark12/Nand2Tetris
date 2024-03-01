from enum import Enum
from typing import Callable, List, Union

from compiler.tokenizer import TokenType


class RuleError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class RuleElementType(Enum):
    # ex) 'class'
    # token type should be keyword, symbol, integerConstant, stringConstant, idenifier
    FIXED_TERMINAL = 0
    # ex) className
    VAR_TERMINAL = 1
    NON_TERMINAL = 2
    # ex) ()
    UNION = 3
    OR = 4
    ZERO_OR_ONE = 5
    MULTIPLE = 6
    # ex) type
    REF = 7
    LIST = 8
    STRING_CONSTANT = 9
    INTEGER_CONSTANT = 10


class RuleElement:
    def __init__(self, rule_element_type: RuleElementType, desc: str):
        self.element_type = rule_element_type
        self.desc = desc

    def compare_with_token(self, token: str) -> bool:
        if self.element_type == RuleElementType.FIXED_TERMINAL:
            return token == self.desc
        elif self.element_type == RuleElementType.VAR_TERMINAL:
            return True
        raise NotImplementedError("Need to implement")


# ex) classVarDec*
class MultipleRuleElement(RuleElement):
    def __init__(self, desc: str, ref: Union[RuleElement, Callable]):
        super().__init__(rule_element_type=RuleElementType.MULTIPLE, desc=desc)
        self.ref = ref


class ZeroOneRuleElement(RuleElement):
    def __init__(self, desc: str, ref: Union[RuleElement, Callable]):
        super().__init__(rule_element_type=RuleElementType.ZERO_OR_ONE, desc=desc)
        self.ref = ref


# ex) group rule elements as list
class ListRuleElement(RuleElement):
    def __init__(self, desc: str, rules: List[RuleElement]):
        super().__init__(rule_element_type=RuleElementType.LIST, desc=desc)
        self.rules = rules


# ex) type
# type => 'int' | 'char' | 'boolean' | className
class RefRuleElement(RuleElement):
    def __init__(self, desc: str, ref: Union[RuleElement, Callable]):
        super().__init__(rule_element_type=RuleElementType.REF, desc=desc)
        self.ref = ref

    def compare_with_token(self, token: str) -> bool:
        return self.ref.compare_with_token(token)


# ex) 'static' | 'field'
class OrRuleElement(RuleElement):
    def __init__(self, desc: str, or_elements: List[RuleElement]):
        super().__init__(rule_element_type=RuleElementType.OR, desc=desc)
        self.or_elements = or_elements

    def compare_with_token(self, token: str) -> bool:
        for element in self.or_elements:
            if element.compare_with_token(token) is True:
                return True
        return False
