import re

class Token:
    def __init__(self, type, lexeme, line, column):
        self.type = type
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, '{self.lexeme}', Line {self.line}, Col {self.column})"

class LexicalError(Exception):
    pass

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_position = 0
        self.token_specs = [
            ('COMMENT',         r'//.*?(\r\n?|\n)|/\*[\s\S]*?\*/'),
            ('WHITESPACE',      r'[ \t\n\r]+'),
            ('FLOAT_KEYWORD',   r'\bfloat\b'),
            ('INT_KEYWORD',     r'\bint\b'),
            ('DO_KEYWORD',      r'\bdo\b'),
            ('WHILE_KEYWORD',   r'\bwhile\b'),
            ('IF_KEYWORD',      r'\bif\b'),
            ('ELSE_KEYWORD',    r'\belse\b'),
            ('FLOAT_LITERAL',   r'\d+\.\d+'),
            ('INT_LITERAL',     r'\d+'),
            ('IDENTIFIER',      r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('PLUS',            r'\+'),
            ('MINUS',           r'-'),
            ('MULTIPLY',        r'\*'),
            ('DIVIDE',          r'/'),
            ('ASSIGN',          r'='),
            ('SEMICOLON',       r';'),
            ('LPAREN',          r'\('),
            ('RPAREN',          r'\)'),
            ('LBRACE',          r'\{'),
            ('RBRACE',          r'\}'),
            ('LESS_EQUAL',      r'<='), 
            ('GREATER_EQUAL',   r'>=' ),
            ('LESS_THAN',       r'<'),
            ('GREATER_THAN',    r'>'),
            ('EQUAL_EQUAL',     r'=='),
            ('NOT_EQUAL',       r'!='), 
            ('MISMATCH',        r'.')  # Catch-all for unexpected characters
        ]
        self.token_regex = re.compile('|'.join(f'(?P<{spec[0]}>{spec[1]})' for spec in self.token_specs))

    def tokenize(self):
        self.tokens = []
        self.current_position = 0
        line_num = 1
        line_start = 0

        while self.current_position < len(self.source_code):
            match = self.token_regex.match(self.source_code, self.current_position)
            if match:
                token_type = match.lastgroup
                lexeme = match.group(token_type)
                column = self.current_position - line_start + 1

                # Handling line number updates for whitespace and comments
                if token_type == 'WHITESPACE' or token_type == 'COMMENT':
                    temp_lexeme_for_newlines = lexeme.replace('\r\n', '\n').replace('\r', '\n')
                    total_newlines = temp_lexeme_for_newlines.count('\n')

                    if total_newlines > 0:
                        line_num += total_newlines
                        last_newline_in_lexeme_idx = -1
                        idx_n = lexeme.rfind('\n')
                        if idx_n > -1:
                            last_newline_in_lexeme_idx = max(last_newline_in_lexeme_idx, idx_n)
                        idx_r = lexeme.rfind('\r')
                        if idx_r > -1:
                            if idx_r + 1 < len(lexeme) and lexeme[idx_r+1] == '\n':
                                pass
                            else:
                                last_newline_in_lexeme_idx = max(last_newline_in_lexeme_idx, idx_r)
                        if last_newline_in_lexeme_idx != -1:
                             line_start = self.current_position + last_newline_in_lexeme_idx + 1
                # Handle MISMATCH for unrecognized characters
                elif token_type == 'MISMATCH':
                    raise LexicalError(f"Unexpected character: '{lexeme}' at line {line_num}, column {column}")
                else:
                    # Add recognized token to the list
                    self.tokens.append(Token(token_type, lexeme, line_num, column))

                # Update the current position in the source code
                self.current_position = match.end()
            else:
                # If no match is found, throw a lexical error
                raise LexicalError(f"Unexpected character at position {self.current_position} (source index) on line {line_num}, near column {self.current_position - line_start + 1}")

        # Add EOF token at the end
        eof_column = self.current_position - line_start + 1
        self.tokens.append(Token('EOF', 'EOF', line_num, eof_column))

        return self.tokens
