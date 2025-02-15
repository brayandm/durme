from .ast import (
    ASTNode,
    ConditionNode,
    DeclarationNode,
    IfNode,
    IncrementNode,
    OperationNode,
    PrintNode,
    ProgramNode,
)


class Transpiler:
    def transpile(self, node: ASTNode) -> str:
        method_name = f"transpile_{node.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.unsupported_node)
        return method(node)

    def transpile_programnode(self, node: ProgramNode) -> str:
        code = "\n".join(self.transpile(stmt) for stmt in node.statements)
        return (
            "#include <iostream>\n\nint main() {\n" + code + "\n return 0;\n}"
        )

    def transpile_declarationnode(self, node: DeclarationNode) -> str:
        return (
            f"{node.var_type} {node.var_name} = {self.transpile(node.value)};"
        )

    def transpile_ifnode(self, node: IfNode) -> str:
        condition = self.transpile(node.condition)
        body = "\n".join(
            "    " + self.transpile(stmt) for stmt in node.body.statements
        )
        return f"if ({condition}) {{\n{body}\n}}"

    def transpile_conditionnode(self, node: ConditionNode) -> str:
        if isinstance(node.left, ASTNode):
            left = self.transpile(node.left)
        else:
            left = str(node.left)

        if isinstance(node.right, ASTNode):
            right = self.transpile(node.right)
        else:
            right = str(node.right)

        operator = node.operator
        return f"({left} {operator} {right})"

    def transpile_incrementnode(self, node: IncrementNode) -> str:
        return f"{node.var_name}++;"

    def transpile_printnode(self, node: PrintNode) -> str:
        return f"std::cout << {node.var_name} << std::endl;"

    def transpile_operationnode(self, node: OperationNode) -> str:
        if isinstance(node.left, ASTNode):
            left = self.transpile(node.left)
        else:
            left = str(node.left)

        if isinstance(node.right, ASTNode):
            right = self.transpile(node.right)
        else:
            right = str(node.right)

        operator = node.operator
        return f"({left} {operator} {right})"

    def unsupported_node(self, node: ASTNode) -> str:
        raise ValueError(f"Unsupported AST node type: {type(node)}")
