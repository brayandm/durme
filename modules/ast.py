from typing import List


class ASTNode:
    def to_string(self, depth: int = 0) -> str:
        """Return a string representation of the node."""
        raise NotImplementedError


class ProgramNode(ASTNode):
    def __init__(self, statements: List[ASTNode]) -> None:
        self.statements = statements

    def to_string(self, depth: int = 0) -> str:
        indent = "  " * depth
        result = f"{indent}ProgramNode:\n"
        for stmt in self.statements:
            result += stmt.to_string(depth + 1)
        return result


class DeclarationNode(ASTNode):
    def __init__(self, var_type: str, var_name: str, value: int) -> None:
        self.var_type = var_type
        self.var_name = var_name
        self.value = value

    def to_string(self, depth: int = 0) -> str:
        indent = "  " * depth
        return f"{indent}DeclarationNode: {self.var_type} {self.var_name} = {self.value}\n"


class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, body: ProgramNode) -> None:
        self.condition = condition
        self.body = body

    def to_string(self, depth: int = 0) -> str:
        indent = "  " * depth
        result = f"{indent}IfNode:\n"
        result += (
            f"{indent}  Condition:\n{self.condition.to_string(depth + 2)}"
        )
        result += f"{indent}  Body:\n{self.body.to_string(depth + 2)}"
        return result


class ConditionNode(ASTNode):
    def __init__(self, left: str, operator: str, right: int) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def to_string(self, depth: int = 0) -> str:
        indent = "  " * depth
        return f"{indent}ConditionNode: {self.left} {self.operator} {self.right}\n"


class IncrementNode(ASTNode):
    def __init__(self, var_name: str) -> None:
        self.var_name = var_name

    def to_string(self, depth: int = 0) -> str:
        indent = "  " * depth
        return f"{indent}IncrementNode: {self.var_name}++\n"
