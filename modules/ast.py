from typing import List


class ASTNode:
    pass


class ProgramNode(ASTNode):
    def __init__(self, statements: List[ASTNode]) -> None:
        self.statements = statements


class DeclarationNode(ASTNode):
    def __init__(self, var_type: str, var_name: str, value: int) -> None:
        self.var_type = var_type
        self.var_name = var_name
        self.value = value


class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, body: ProgramNode) -> None:
        self.condition = condition
        self.body = body


class ConditionNode(ASTNode):
    def __init__(self, left: str, operator: str, right: int) -> None:
        self.left = left
        self.operator = operator
        self.right = right


class IncrementNode(ASTNode):
    def __init__(self, var_name: str) -> None:
        self.var_name = var_name
