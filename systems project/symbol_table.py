# symbol_table.py

# Removed: from semantic_analyzer import SemanticError
# SemanticError is now defined in semantic_analyzer.py and imported by test.py and semantic_analyzer.py

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, attributes):
        # We can still raise SemanticError here because semantic_analyzer.py
        # will have imported SemanticError before importing SymbolTable.
        # However, to be completely safe and break the cycle, you could
        # define a basic error class here or raise a generic Exception,
        # but raising SemanticError is fine in this structure.
        from semantic_analzer import SemanticError # Import locally to avoid circular dependency at load time
        if name in self.symbols:
            raise SemanticError(f"Variable '{name}' already declared.")
        self.symbols[name] = attributes

    def get_symbol(self, name):
        return self.symbols.get(name)

    def has_symbol(self, name):
        return name in self.symbols
