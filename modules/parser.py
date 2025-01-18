from typing import Any, Optional

import ply.yacc as yacc  # type: ignore

from .ast import (
    ConditionNode,
    DeclarationNode,
    IfNode,
    IncrementNode,
    ProgramNode,
)
from .lexer import tokens

_ = tokens


def p_program(p: Any) -> None:
    """
    program : statement
            | statement program
    """
    if len(p) == 2:
        p[0] = ProgramNode([p[1]])
    else:
        p[0] = ProgramNode([p[1]] + p[2].statements)


def p_statement_declaration(p: Any) -> None:
    "statement : INT ID ASSIGN NUMBER SEMICOLON"
    p[0] = DeclarationNode("int", p[2], p[4])


def p_statement_if(p: Any) -> None:
    "statement : IF LPAREN condition RPAREN LBRACE program RBRACE"
    p[0] = IfNode(p[3], p[6])


def p_condition(p: Any) -> None:
    "condition : ID LT NUMBER"
    p[0] = ConditionNode(p[1], "<", p[3])


def p_statement_increment(p: Any) -> None:
    "statement : ID INCREMENT SEMICOLON"
    p[0] = IncrementNode(p[1])


def p_error(p: Optional[Any]) -> None:
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()
