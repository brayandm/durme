from typing import Any, Optional

import ply.yacc as yacc  # type: ignore

from .ast import (
    ConditionNode,
    DeclarationNode,
    IfNode,
    IncrementNode,
    OperationNode,
    PrintNode,
    ProgramNode,
)
from .lexer import Lexer


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)

    def parse(self, data: str) -> Optional[ProgramNode]:
        """Parse the input data and return the AST."""
        self.lexer.input(data)
        return self.parser.parse(lexer=self.lexer.lexer)  # type: ignore

    def p_program(self, p: Any) -> None:
        """
        program : statement
                | statement program
        """
        if len(p) == 2:
            p[0] = ProgramNode([p[1]])
        else:
            p[0] = ProgramNode([p[1]] + p[2].statements)

    def p_statement_declaration(self, p: Any) -> None:
        "statement : INT ID ASSIGN expression SEMICOLON"
        p[0] = DeclarationNode("int", p[2], p[4])

    def p_statement_if(self, p: Any) -> None:
        "statement : IF LPAREN condition RPAREN LBRACE program RBRACE"
        p[0] = IfNode(p[3], p[6])

    def p_condition(self, p: Any) -> None:
        "condition : expression LT expression"
        p[0] = ConditionNode(p[1], "<", p[3])

    def p_statement_print(self, p: Any) -> None:
        "statement : PRINT LPAREN expression RPAREN SEMICOLON"
        p[0] = PrintNode(p[3])

    def p_statement_increment(self, p: Any) -> None:
        "statement : ID INCREMENT SEMICOLON"
        p[0] = IncrementNode(p[1])

    def p_expression(self, p: Any) -> None:
        """
        expression : expression ADD term
                   | expression SUB term
                   | term
        """
        if len(p) == 4:
            if p[2] == "+":
                p[0] = OperationNode(p[1], "+", p[3])
            elif p[2] == "-":
                p[0] = OperationNode(p[1], "-", p[3])
        else:
            p[0] = p[1]

    def p_term(self, p: Any) -> None:
        """
        term : term MUL factor
             | term DIV factor
             | factor
        """
        if len(p) == 4:
            if p[2] == "*":
                p[0] = OperationNode(p[1], "*", p[3])
            elif p[2] == "/":
                p[0] = OperationNode(p[1], "/", p[3])
        else:
            p[0] = p[1]

    def p_factor(self, p: Any) -> None:
        """
        factor : LPAREN expression RPAREN
               | NUMBER
               | ID
        """
        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = p[1]

    def p_error(self, p: Optional[Any]) -> None:
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")
