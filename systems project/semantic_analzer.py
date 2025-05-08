# semantic_analyzer.py

from ast_nodes import (
    ProgramNode, StatementListNode, DeclarationNode, AssignmentNode, DoWhileNode,
    BinaryOpNode, IntLiteralNode, FloatLiteralNode, IdentifierNode,
    ASTNode
)
# Import SymbolTable, but SemanticError is defined here
from symbol_table import SymbolTable

# Define SemanticError here
class SemanticError(Exception):
    pass


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, ast_root):
        print("\n--- Semantic Analysis ---")
        self.visit(ast_root)
        print("Semantic analysis completed successfully.")
        print("--- Symbol Table ---")
        for name, attributes in self.symbol_table.symbols.items():
            print(f"Variable: {name}, Type: {attributes.get('type')}")
        print("----------------------")


    def visit(self, node):
        if node is None:
            return None

        method_name = 'visit_' + type(node).__name__
        visitor_method = getattr(self, method_name, self.generic_visit)
        return visitor_method(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)
        return None

    def visit_ProgramNode(self, node):
        self.generic_visit(node)

    def visit_StatementListNode(self, node):
        self.generic_visit(node)

    def visit_DeclarationNode(self, node):
        if self.symbol_table.has_symbol(node.identifier_token.lexeme):
            raise SemanticError(f"Variable '{node.identifier_token.lexeme}' already declared at line {node.identifier_token.line}, column {node.identifier_token.column}")

        declared_type = node.type_token.lexeme

        self.symbol_table.add_symbol(node.identifier_token.lexeme, {'type': declared_type})
        print(f"Semantic: Declared variable '{node.identifier_token.lexeme}' with type '{declared_type}'")

        if node.assignment_expr:
            assigned_type = self.visit(node.assignment_expr)
            if declared_type == 'int' and assigned_type == 'float':
                raise SemanticError(f"Cannot assign float to int variable '{node.identifier_token.lexeme}' at line {node.identifier_token.line}, column {node.identifier_token.column}")


    def visit_AssignmentNode(self, node):
        var_name = node.identifier_token.lexeme
        symbol_info = self.symbol_table.get_symbol(var_name)
        if not symbol_info:
            raise SemanticError(f"Undeclared variable '{var_name}' at line {node.identifier_token.line}, column {node.identifier_token.column}")

        declared_type = symbol_info['type']

        assigned_type = self.visit(node.assignment_expr)

        if declared_type == 'int' and assigned_type == 'float':
            raise SemanticError(f"Cannot assign float to int variable '{var_name}' at line {node.identifier_token.line}, column {node.identifier_token.column}")

        print(f"Semantic: Checked assignment for '{var_name}'")


    def visit_DoWhileNode(self, node):
        self.visit(node.body)

        condition_type = self.visit(node.condition)

        if condition_type not in ['int', 'float']:
            condition_token = node.condition.token if node.condition and node.condition.token else "unknown location"
            line = getattr(condition_token, 'line', 'unknown')
            column = getattr(condition_token, 'column', 'unknown')
            raise SemanticError(f"Do-while condition must be of numeric type (int or float), found '{condition_type}' at line {line}, column {column}")

        print("Semantic: Checked do-while loop.")


    def visit_BinaryOpNode(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        operator = node.operator_token.lexeme

        if left_type == 'float' or right_type == 'float':
            result_type = 'float'
        elif left_type == 'int' and right_type == 'int':
            result_type = 'int'
        else:
            raise SemanticError(f"Invalid operand types for operator '{operator}': '{left_type}' and '{right_type}' at line {node.operator_token.line}, column {node.operator_token.column}")

        if operator in ('+', '-', '*', '/'):
             if left_type not in ['int', 'float'] or right_type not in ['int', 'float']:
                 raise SemanticError(f"Arithmetic operator '{operator}' requires numeric operands, found '{left_type}' and '{right_type}' at line {node.operator_token.line}, column {node.operator_token.column}")
        elif operator in ('<', '>', '<=', '>=', '==', '!='):
            if left_type not in ['int', 'float'] or right_type not in ['int', 'float']:
                 raise SemanticError(f"Comparison operator '{operator}' requires numeric operands, found '{left_type}' and '{right_type}' at line {node.operator_token.line}, column {node.operator_token.column}")
            result_type = 'int'

        print(f"Semantic: Checked binary operation '{operator}' with operand types '{left_type}' and '{right_type}', resulting type '{result_type}'")
        return result_type


    def visit_IntLiteralNode(self, node):
        print(f"Semantic: Found IntLiteral with value {node.value}")
        return 'int'

    def visit_FloatLiteralNode(self, node):
        print(f"Semantic: Found FloatLiteral with value {node.value}")
        return 'float'

    def visit_IdentifierNode(self, node):
        var_name = node.name
        symbol_info = self.symbol_table.get_symbol(var_name)
        if not symbol_info:
            raise SemanticError(f"Undeclared variable '{var_name}' at line {node.token.line}, column {node.token.column}")

        print(f"Semantic: Found Identifier '{var_name}' with type '{symbol_info['type']}'")
        return symbol_info['type']
