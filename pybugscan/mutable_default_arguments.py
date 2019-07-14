import ast
from enum import Enum

from pybugscan.core import BugScanner

# These nodes are definitely mutable
MUTABLE_CANDIDATES = {
    ast.List,
    ast.Dict,
    ast.Set,
    ast.ListComp,
    ast.DictComp,
    ast.SetComp,
    ast.GeneratorExp,
    ast.Call,
    ast.Name,
}

class Mutability(Enum):
    MUTABLE = "Mutable"
    POSSIBLY_MUTABLE = "Possibly mutable"
    IMMUTABLE = "Immutable"


def format_variable(node: ast.Name) -> (str, Mutability):
    """Formats a variable (i.e. a Name)"""
    return f"variable '{node.id}' in outer scope", Mutability.POSSIBLY_MUTABLE


def format_call(node: ast.Call) -> (str, Mutability):
    """Formats a function call"""
    try:
        func = node.func.id
    except AttributeError:
        return type(node).__name__, Mutability.POSSIBLY_MUTABLE
    if func == 'dict':
        return "empty dict", Mutability.MUTABLE
    elif func == 'set':
        return "empty set", Mutability.MUTABLE
    elif func == 'list':
        return "empty list", Mutability.MUTABLE
    elif func == 'tuple':
        return "empty tuple", Mutability.IMMUTABLE
    return f"function call", Mutability.POSSIBLY_MUTABLE


def format_iterable(node: ast.AST, elements_name='elts') -> (str, Mutability):
    """Formats an iterable node"""
    datatype = type(node).__name__.lower()
    num_elements = len(getattr(node, elements_name))
    if num_elements == 0:
        return f"empty {datatype}", Mutability.MUTABLE
    elif num_elements == 1:
        return f"{datatype} with 1 element", Mutability.MUTABLE
    else:
        return f"{datatype} with {num_elements} elements", Mutability.MUTABLE

def format_dict(node: ast.Dict) -> (str, Mutability):
    """Formats a dict node"""
    return format_iterable(node, 'keys')

def format_list(node: ast.List) -> (str, Mutability):
    """Formats a list node"""
    return format_iterable(node, 'elts')

def format_set(node: ast.Set) -> (str, Mutability):
    """Formats a set node"""
    return format_iterable(node, 'elts')

def format_arg(node: ast.AST) -> (str, Mutability):
    """Formats a node"""
    if isinstance(node, ast.Name):
        return format_variable(node)
    elif isinstance(node, ast.Call):
        return format_call(node)
    elif isinstance(node, ast.Set):
        return format_set(node)
    elif isinstance(node, ast.List):
        return format_list(node)
    elif isinstance(node, ast.Dict):
        return format_dict(node)
    elif isinstance(node, ast.ListComp):
        return "list comprehension", Mutability.MUTABLE
    elif isinstance(node, ast.DictComp):
        return "dict comprehension", Mutability.MUTABLE
    elif isinstance(node, ast.SetComp):
        return "set comprehension", Mutability.MUTABLE
    elif isinstance(node, ast.GeneratorExp):
        return "generator expression", Mutability.MUTABLE
    else:
        return type(node).__name__, Mutability.IMMUTABLE

class MutableDefaultArgumentFinder(BugScanner):
    bug_type = "Mutable default arguments"
    bug_description = """Default arguments are created at the same time as the function, and will always refer to the same instance. See https://docs.python-guide.org/writing/gotchas/"""

    def __init__(self, args):
        super().__init__(args)
        if self.args.get('possibly_mutable', False):
            self.mutability_criterion = { Mutability.MUTABLE, Mutability.POSSIBLY_MUTABLE }
        else:
            self.mutability_criterion = { Mutability.MUTABLE, }

    def visit_FunctionDef(self, node):
        for default in node.args.defaults:
            for mmut in MUTABLE_CANDIDATES:
                if isinstance(default, mmut):
                    formatted, mutability = format_arg(default)
                    if mutability in self.mutability_criterion:
                        self.warnings.append(
                            f"{mutability.value} default argument "
                            f"in {node.name} (line {node.lineno}): "
                            f"{formatted}"
                        )
