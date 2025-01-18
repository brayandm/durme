from .ast import (
    ASTNode,
    ConditionNode,
    DeclarationNode,
    IfNode,
    IncrementNode,
    ProgramNode,
)


class Transpiler:
    def transpile(self, node: ASTNode) -> str:
        method_name = f"transpile_{node.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.unsupported_node)
        return method(node)

    def transpile_programnode(self, node: ProgramNode) -> str:
        return "\n".join(self.transpile(stmt) for stmt in node.statements)

    def transpile_declarationnode(self, node: DeclarationNode) -> str:
        return f"{node.var_type} {node.var_name} = {node.value};"

    def transpile_ifnode(self, node: IfNode) -> str:
        condition = self.transpile(node.condition)
        body = "\n".join(
            "    " + self.transpile(stmt) for stmt in node.body.statements
        )
        return f"if ({condition}) {{\n{body}\n}}"

    def transpile_conditionnode(self, node: ConditionNode) -> str:
        return f"{node.left} {node.operator} {node.right}"

    def transpile_incrementnode(self, node: IncrementNode) -> str:
        return f"{node.var_name}++;"

    def unsupported_node(self, node: ASTNode) -> str:
        raise ValueError(f"Unsupported AST node type: {type(node)}")
