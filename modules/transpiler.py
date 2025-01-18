from .ast import (
    ASTNode,
    ConditionNode,
    DeclarationNode,
    IfNode,
    IncrementNode,
    ProgramNode,
)


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
