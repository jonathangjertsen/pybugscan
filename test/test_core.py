import ast

from pybugscan import core

def test_parse_source():
    """Check that we can parse some code"""
    tree = core.parse_source("x = 2")
    assert isinstance(tree, ast.AST)


def test_parse_file(source_file):
    """Check that we can parse a file"""
    source = source_file("dumbness.py")
    tree = core.parse_file(source)
    assert isinstance(tree, ast.AST)