from enum import StrEnum


class SymbolKind(StrEnum):
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"
    INTERFACE = "interface"
    VARIABLE = "variable"
    PROPERTY = "property"
    ENUM = "enum"
