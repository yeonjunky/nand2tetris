from enum import Enum

class Keyword(Enum):
    CLASS = 1
    METHOD = 2
    FUNCTION = 3
    CONSTRUCOTR = 4
    INT = 5
    BOOLEAN = 6
    CHAR = 7
    VOID = 8
    VAR = 9
    STATIC = 10
    FIELD = 11
    LET = 12
    DO = 13
    IF = 14
    ELSE = 15
    WHILE = 16
    RETURN = 17
    TRUE = 18
    FALSE = 19
    NULL = 20
    THIS = 21

class Tokentype(Enum):
    KEYWORD = 1
    SYMBOL = 2
    IDENTIFIER = 3
    INT_CONST = 4
    STRING_CONST = 5

class Kind(Enum):
    STATIC = 1
    FIELD = 2
    ARG = 3
    VAR = 4

class Segment(Enum):
    CONST = 1
    ARG = 2
    LOCAL = 3
    STATIC = 4
    THIS = 5
    THAT = 6
    POINTER = 7
    TEMP = 8

class Command(Enum):
    ADD = 1
    SUB = 2
    NEG = 3
    EQ = 4
    GT = 5
    LT = 6
    AND = 7
    OR = 8
    NOT = 9
