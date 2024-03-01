from compiler.rule import (
    OrRuleElement,
    RefRuleElement,
    RuleElement,
    RuleElementType,
    RuleError,
    ZeroOneRuleElement,
)

TYPE_RULE_ELEMENTS = RefRuleElement(
    desc="type",
    ref=OrRuleElement(
        desc="'int' | 'char' | 'boolean' | className",
        or_elements=[
            RuleElement(RuleElementType.FIXED_TERMINAL, "int"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "char"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "boolean"),
            RuleElement(RuleElementType.VAR_TERMINAL, "className"),
        ],
    ),
)

KEYWORD_CONSTANT_RULE_ELEMENTS = RefRuleElement(
    desc="keywordConstant",
    ref=OrRuleElement(
        desc="'true' | 'false' | 'null' | 'this'",
        or_elements=[
            RuleElement(RuleElementType.FIXED_TERMINAL, "true"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "false"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "null"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "this"),
        ],
    ),
)

OP_RULE_ELEMENTS = RefRuleElement(
    desc="op",
    ref=OrRuleElement(
        desc="'+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='",
        or_elements=[
            RuleElement(RuleElementType.FIXED_TERMINAL, "+"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "-"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "*"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "/"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "&"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "|"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "<"),
            RuleElement(RuleElementType.FIXED_TERMINAL, ">"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "="),
        ],
    ),
)


UNARY_OP_RULE_ELEMENTS = RefRuleElement(
    desc="unary OP",
    ref=OrRuleElement(
        desc="'-' | '~'",
        or_elements=[
            RuleElement(RuleElementType.FIXED_TERMINAL, "-"),
            RuleElement(RuleElementType.FIXED_TERMINAL, "~"),
        ],
    ),
)
