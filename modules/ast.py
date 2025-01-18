from typing import List


class ASTNode:
    def print(self, depth: int = 0) -> None:
        """Print the node and its children."""
        raise NotImplementedError


class ProgramNode(ASTNode):
    def __init__(self, statements: List[ASTNode]) -> None:
        self.statements = statements

    def print(self, depth: int = 0) -> None:
        indent = "  " * depth
        print(f"{indent}ProgramNode:")
        for stmt in self.statements:
            stmt.print(depth + 1)


class DeclarationNode(ASTNode):
    def __init__(self, var_type: str, var_name: str, value: int) -> None:
        self.var_type = var_type
        self.var_name = var_name
        self.value = value

    def print(self, depth: int = 0) -> None:
        indent = "  " * depth
        print(
            f"{indent}DeclarationNode: {self.var_type} {self.var_name} = {self.value}"
        )


class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, body: ProgramNode) -> None:
        self.condition = condition
        self.body = body

    def print(self, depth: int = 0) -> None:
        indent = "  " * depth
        print(f"{indent}IfNode:")
        print(f"{indent}  Condition:")
        self.condition.print(depth + 2)
        print(f"{indent}  Body:")
        self.body.print(depth + 2)


class ConditionNode(ASTNode):
    def __init__(self, left: str, operator: str, right: int) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def print(self, depth: int = 0) -> None:
        indent = "  " * depth
        print(
            f"{indent}ConditionNode: {self.left} {self.operator} {self.right}"
        )


class IncrementNode(ASTNode):
    def __init__(self, var_name: str) -> None:
        self.var_name = var_name

    def print(self, depth: int = 0) -> None:
        indent = "  " * depth
        print(f"{indent}IncrementNode: {self.var_name}++")
