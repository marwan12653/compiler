from lexical import Lexer, Token
from ast_nodes import (
    ProgramNode, StatementListNode, DeclarationNode, AssignmentNode, DoWhileNode,
    BinaryOpNode, IntLiteralNode, FloatLiteralNode, IdentifierNode,
    ExpressionNode, FactorNode
)

class SyntaxError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def match(self, *expected_types):
        if self.current < len(self.tokens) and self.tokens[self.current].type in expected_types:
            token = self.tokens[self.current]
            self.current += 1
            return token
        return None

    def expect(self, expected_type):
        token = self.match(expected_type)
        if not token:
            current_token = self.tokens[self.current] if self.current < len(self.tokens) else "End of input"
            raise SyntaxError(f"Expected {expected_type} but found {current_token} at line {current_token.line}, column {current_token.column}")
        return token

    def parse(self):
        return self.program()

    def program(self):
        program_node = ProgramNode()
        program_node.add_child(self.statement_list(['EOF']))
        return program_node

    def statement_list(self, stop_types):
        statement_list_node = StatementListNode()
        while self.tokens[self.current].type not in stop_types:
            statement_list_node.add_child(self.statement())
        return statement_list_node

    def statement(self):
        if self.tokens[self.current].type in ['INT_KEYWORD', 'FLOAT_KEYWORD']:
            return self.declaration()
        elif self.tokens[self.current].type == 'IDENTIFIER':
            return self.assignment()
        elif self.tokens[self.current].type == 'DO_KEYWORD':
            return self.do_while_statement()
        else:
            current_token = self.tokens[self.current] if self.current < len(self.tokens) else "End of input"
            raise SyntaxError(f"Unexpected statement: {current_token} at line {current_token.line}, column {current_token.column}")

    def declaration(self):
        type_token = self.match('INT_KEYWORD', 'FLOAT_KEYWORD')
        identifier_token = self.expect('IDENTIFIER')
        assignment_expr = None
        if self.match('ASSIGN'):
            assignment_expr = self.expr()
        self.expect('SEMICOLON')
        return DeclarationNode(type_token, identifier_token, assignment_expr)

    def assignment(self):
        identifier_token = self.expect('IDENTIFIER')
        self.expect('ASSIGN')
        assignment_expr = self.expr()
        self.expect('SEMICOLON')
        return AssignmentNode(identifier_token, assignment_expr)

    def do_while_statement(self):
        self.expect('DO_KEYWORD')
        self.expect('LBRACE')
        body = self.statement_list(['RBRACE'])
        self.expect('RBRACE')
        self.expect('WHILE_KEYWORD')
        self.expect('LPAREN')
        condition = self.expr()
        self.expect('RPAREN')
        self.expect('SEMICOLON')
        return DoWhileNode(body, condition)

    def expr(self):
        left_node = self.arithmetic_expr()

        while self.tokens[self.current].type in ('LESS_EQUAL', 'GREATER_EQUAL', 'LESS_THAN', 'GREATER_THAN', 'EQUAL_EQUAL', 'NOT_EQUAL'):
            operator = self.tokens[self.current]
            self.current += 1
            right_node = self.arithmetic_expr()
            left_node = BinaryOpNode(left_node, operator, right_node)

        return left_node

    def arithmetic_expr(self):
        left_node = self.term()

        while self.tokens[self.current].type in ('PLUS', 'MINUS'):
            operator = self.tokens[self.current]
            self.current += 1
            right_node = self.term()
            left_node = BinaryOpNode(left_node, operator, right_node)

        return left_node

    def term(self):
        left_node = self.factor()

        while self.tokens[self.current].type in ('MULTIPLY', 'DIVIDE'):
            operator = self.tokens[self.current]
            self.current += 1
            right_node = self.factor()
            left_node = BinaryOpNode(left_node, operator, right_node)

        return left_node

    def factor(self):
        if self.tokens[self.current].type in ('INT_LITERAL'):
            token = self.match('INT_LITERAL')
            return IntLiteralNode(token)
        elif self.tokens[self.current].type in ('FLOAT_LITERAL'):
             token = self.match('FLOAT_LITERAL')
             return FloatLiteralNode(token)
        elif self.tokens[self.current].type in ('IDENTIFIER'):
            token = self.match('IDENTIFIER')
            return IdentifierNode(token)
        elif self.match('LPAREN'):
            expr_node = self.expr()
            self.expect('RPAREN')
            return expr_node
        else:
            current_token = self.tokens[self.current] if self.current < len(self.tokens) else "End of input"
            raise SyntaxError(f"Unexpected factor: {current_token} at line {current_token.line}, column {current_token.column}")
