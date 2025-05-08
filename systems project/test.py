from lexical import Lexer, LexicalError
from parser import Parser, SyntaxError
from ast_nodes import ASTNode 
from semantic_analzer import SemanticAnalyzer, SemanticError

def print_ast(node, level=0):
    """Recursively prints the AST structure."""
    indent = "  " * level
    if isinstance(node, ASTNode):
        print(f"{indent}{node}")
        for child in node.children:
            print_ast(child, level + 1)
    elif isinstance(node, list):
         print(f"{indent}Children:")
         for item in node:
             print_ast(item, level + 1)
    elif node is not None:
         print(f"{indent}{node}")


def main():
    file_path = "sample.txt"
    print(f"Reading source file: '{file_path}'")

    try:
        with open(file_path, 'r') as file:
            source_code = file.read()

        print("\n--- Source Code ---")
        print(source_code)
        print("----------------------\n")

        # Initialize the lexer
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        print("--- Tokens ---")
        for token in tokens:
            print(token)

        print("\nSyntax Analysis (Building AST) ---")
        # Initialize the parser
        parser = Parser(tokens)
        ast_root = parser.parse()

        print("\n--- Abstract Syntax Tree ---")
        print_ast(ast_root)
        print("--------------------------\n")

        # --- Semantic Analysis ---
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.analyze(ast_root)
        # --- End Semantic Analysis ---


    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
    except LexicalError as e:
        print(f"Lexical Error: {e}")
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except SemanticError as e: # Catch SemanticError
        print(f"Semantic Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()
