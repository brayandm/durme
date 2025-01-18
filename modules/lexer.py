from typing import Any, Dict

import ply.lex as lex  # type: ignore

tokens = [
    "INT",
    "ID",
    "ASSIGN",
    "NUMBER",
    "IF",
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    "LT",
    "INCREMENT",
    "SEMICOLON",
]

t_ASSIGN = r"="
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LT = r"<"
t_INCREMENT = r"\+\+"
t_SEMICOLON = r";"
t_ignore = " \t"

reserved: Dict[str, str] = {"int": "INT", "if": "IF"}


def t_ID(t: Any) -> Any:
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    t.type = reserved.get(t.value, "ID")
    return t


def t_NUMBER(t: Any) -> Any:
    r"\d+"
    t.value = int(t.value)
    return t


def t_newline(t: Any) -> None:
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t: Any) -> None:
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()
