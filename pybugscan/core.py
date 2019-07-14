import ast
from typing import Optional


def parse_source(source_str: str) -> ast.AST:
    """Parses a piece of source code and returns the AST"""
    return ast.parse(source_str)


def parse_file(filename: str) -> ast.AST:
    """Parses the code in a Python file and returns the AST"""
    with open(filename, "r") as source:
        return parse_source(source.read())


class BugScanner(ast.NodeVisitor):
    analyzers = {}
    bug_type = "Unknown bug"
    bug_description = "This is an unknown bug."

    def __init__(self, args: Optional[dict]=None):
        """Initializes warnings"""
        self.warnings = []
        self.args = args

    def visit_file(self, filename: str):
        """Parses the file and visits the AST"""
        try:
            tree = parse_file(filename)
            self.visit(tree)
        except SyntaxError as se:
            self.warnings.append(f"SyntaxError when parsing {filename}: {se}")

    def clear_warnings(self):
        """Resets the warnings"""
        self.warnings = []

    def get_and_clear_warnings(self):
        """Resets and returns the warnings"""
        result, self.warnings = self.warnings, []
        return result