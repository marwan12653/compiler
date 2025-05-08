class ASTNode:
    def __init__(self, token=None):
        self.token = token
        self.children = []

    def add_child(self, node):
        if node:
            self.children.append(node)

    def __repr__(self):
        return self.__class__.__name__

class ProgramNode(ASTNode):
    pass

class StatementListNode(ASTNode):
    pass

class DeclarationNode(ASTNode):
    def __init__(self, type_token, identifier_token, assignment_expr=None):
        super().__init__(type_token)
        self.type_token = type_token
        self.identifier_token = identifier_token
        self.assignment_expr = assignment_expr
        self.add_child(assignment_expr)

    def __repr__(self):
        return f"Declaration({self.identifier_token.lexeme}: {self.type_token.lexeme})"


class AssignmentNode(ASTNode):
    def __init__(self, identifier_token, assignment_expr):
        super().__init__(identifier_token)
        self.identifier_token = identifier_token
        self.assignment_expr = assignment_expr
        self.add_child(assignment_expr)

    def __repr__(self):
        return f"Assignment({self.identifier_token.lexeme})"


class DoWhileNode(ASTNode):
    def __init__(self, body, condition):
        super().__init__()
        self.body = body
        self.condition = condition
        self.add_child(body)
        self.add_child(condition)

    def __repr__(self):
        return "DoWhile"

class ExpressionNode(ASTNode):
    pass

class BinaryOpNode(ExpressionNode):
    def __init__(self, left, operator_token, right):
        super().__init__(operator_token)
        self.left = left
        self.operator_token = operator_token
        self.right = right
        self.add_child(left)
        self.add_child(right)

    def __repr__(self):
        return f"BinaryOp({self.operator_token.lexeme})"

class FactorNode(ExpressionNode):
    pass

class IntLiteralNode(FactorNode):
    def __init__(self, token):
        super().__init__(token)
        self.value = int(token.lexeme)

    def __repr__(self):
        return f"IntLiteral({self.value})"


class FloatLiteralNode(FactorNode):
    def __init__(self, token):
        super().__init__(token)
        self.value = float(token.lexeme)

    def __repr__(self):
        return f"FloatLiteral({self.value})"


class IdentifierNode(FactorNode):
    def __init__(self, token):
        super().__init__(token)
        self.name = token.lexeme

    def __repr__(self):
        return f"Identifier({self.name})"

