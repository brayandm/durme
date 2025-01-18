from typing import Any, Dict, List, Optional

import ply.lex as lex  # type: ignore
import ply.yacc as yacc  # type: ignore

# Lexer
tokens: List[str] = [
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

t_ASSIGN: str = r"="
t_LPAREN: str = r"\("
t_RPAREN: str = r"\)"
t_LBRACE: str = r"\{"
t_RBRACE: str = r"\}"
t_LT: str = r"<"
t_INCREMENT: str = r"\+\+"
t_SEMICOLON: str = r";"

t_ignore: str = " \t"

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


lexer: Any = lex.lex()


# AST Node Definitions
class ASTNode:
    pass


class ProgramNode(ASTNode):
    def __init__(self, statements: List[ASTNode]) -> None:
        self.statements: List[ASTNode] = statements


class DeclarationNode(ASTNode):
    def __init__(self, var_type: str, var_name: str, value: int) -> None:
        self.var_type: str = var_type
        self.var_name: str = var_name
        self.value: int = value


class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, body: ProgramNode) -> None:
        self.condition: ASTNode = condition
        self.body: ProgramNode = body


class ConditionNode(ASTNode):
    def __init__(self, left: str, operator: str, right: int) -> None:
        self.left: str = left
        self.operator: str = operator
        self.right: int = right


class IncrementNode(ASTNode):
    def __init__(self, var_name: str) -> None:
        self.var_name: str = var_name


# Parser
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


parser: Any = yacc.yacc()


# Transpiler
def transpile_ast(node: ASTNode) -> str:
    if isinstance(node, ProgramNode):
        return "\n".join(transpile_ast(stmt) for stmt in node.statements)
    elif isinstance(node, DeclarationNode):
        return f"{node.var_type} {node.var_name} = {node.value};"
    elif isinstance(node, IfNode):
        condition = transpile_ast(node.condition)
        body = "\n".join(
            "    " + transpile_ast(stmt) for stmt in node.body.statements
        )
        return f"if ({condition}) {{\n{body}\n}}"
    elif isinstance(node, ConditionNode):
        return f"{node.left} {node.operator} {node.right}"
    elif isinstance(node, IncrementNode):
        return f"{node.var_name}++;"
    else:
        raise ValueError(f"Unsupported AST node type: {type(node)}")


# Main
if __name__ == "__main__":
    input_code: str = """
    int a = 3;
    if (a < 7) {
        a++;
    }
    """
    ast: ASTNode = parser.parse(input_code)
    cpp_code: str = transpile_ast(ast)
    print("Generated C++ code:")
    print(cpp_code)
