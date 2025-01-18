import ply.lex as lex  # type: ignore
import ply.yacc as yacc  # type: ignore

# Lexer
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

reserved = {"int": "INT", "if": "IF"}


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    t.type = reserved.get(t.value, "ID")
    return t


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()


# AST Node Definitions
class ASTNode:
    pass


class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class DeclarationNode(ASTNode):
    def __init__(self, var_type, var_name, value):
        self.var_type = var_type
        self.var_name = var_name
        self.value = value


class IfNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ConditionNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class IncrementNode(ASTNode):
    def __init__(self, var_name):
        self.var_name = var_name


# Parser
def p_program(p):
    """
    program : statement
            | statement program
    """
    if len(p) == 2:
        p[0] = ProgramNode([p[1]])
    else:
        p[0] = ProgramNode([p[1]] + p[2].statements)


def p_statement_declaration(p):
    "statement : INT ID ASSIGN NUMBER SEMICOLON"
    p[0] = DeclarationNode("int", p[2], p[4])


def p_statement_if(p):
    "statement : IF LPAREN condition RPAREN LBRACE program RBRACE"
    p[0] = IfNode(p[3], p[6])


def p_condition(p):
    "condition : ID LT NUMBER"
    p[0] = ConditionNode(p[1], "<", p[3])


def p_statement_increment(p):
    "statement : ID INCREMENT SEMICOLON"
    p[0] = IncrementNode(p[1])


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()


# Transpiler
def transpile_ast(node):
    if isinstance(node, ProgramNode):
        return "\n".join(transpile_ast(stmt) for stmt in node.statements)
    elif isinstance(node, DeclarationNode):
        return f"{node.var_type} {node.var_name} = {node.value};"
    elif isinstance(node, IfNode):
        condition = transpile_ast(node.condition)
        body = "\n".join("    " + transpile_ast(stmt) for stmt in node.body.statements)
        return f"if ({condition}) {{\n{body}\n}}"
    elif isinstance(node, ConditionNode):
        return f"{node.left} {node.operator} {node.right}"
    elif isinstance(node, IncrementNode):
        return f"{node.var_name}++;"
    else:
        raise ValueError(f"Unsupported AST node type: {type(node)}")


# Main
if __name__ == "__main__":
    input_code = """
    int a = 3;
    if (a < 7) {
        a++;
    }
    """
    ast = parser.parse(input_code)
    cpp_code = transpile_ast(ast)
    print("Generated C++ code:")
    print(cpp_code)
