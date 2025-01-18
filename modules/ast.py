from typing import List, Union


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
    def __init__(self, var_type: str, var_name: str, value: ASTNode) -> None:
        self.var_type = var_type
        self.var_name = var_name
        self.value = value

    def to_string(self, depth: int = 0) -> str:
        indent = "  " * depth
        result = f"{indent}DeclarationNode:\n"
        result += f"{indent}  Type: {self.var_type}\n"
        result += f"{indent}  Name: {self.var_name}\n"
        result += f"{indent}  {self.value.to_string(depth + 1)}\n"
        return result


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
    def __init__(self, left: ASTNode, operator: str, right: ASTNode) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def to_string(self, depth: int = 0) -> str:
        indent = "  " * depth
        result = f"{indent}ConditionNode: {self.operator}\n"
        if isinstance(self.left, ASTNode):
            result += f"{indent}  {self.left.to_string(depth + 1)}"
        else:
            result += f"{indent}  {self.left}\n"
        if isinstance(self.right, ASTNode):
            result += f"{indent}  {self.right.to_string(depth + 1)}"
        else:
            result += f"{indent}  {self.right}\n"
        return result


class IncrementNode(ASTNode):
    def __init__(self, var_name: str) -> None:
        self.var_name = var_name

    def to_string(self, depth: int = 0) -> str:
        indent = "  " * depth
        return f"{indent}IncrementNode: {self.var_name}++\n"


class PrintNode(ASTNode):
    def __init__(self, var_name: str) -> None:
        self.var_name = var_name

    def to_string(self, depth: int = 0) -> str:
        indent = "  " * depth
        return f"{indent}PrintNode: print({self.var_name})\n"


class OperationNode(ASTNode):
    def __init__(
        self,
        left: Union[int, ASTNode],
        operator: str,
        right: Union[int, ASTNode],
    ) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def to_string(self, depth: int = 0) -> str:
        indent = "  " * depth
        result = f"OperationNode: {self.operator}\n"
        if isinstance(self.left, ASTNode):
            result += f"{indent} {self.left.to_string(depth + 1)}"
        else:
            result += f"{indent} {self.left}\n"

        if isinstance(self.right, ASTNode):
            result += f"{indent} {self.right.to_string(depth + 1)}"
        else:
            result += f"{indent} {self.right}\n"
        return result
