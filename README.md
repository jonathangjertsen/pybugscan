# Python bug scanner

It scans your code for bugs.

Currently there is only one kind of bug that is looked
for: mutable default arguments in function definitions.

This is my first attempt at static analysis, 

## Install

* Clone the repo
* `pip install -e .`

## Run

To run it against some files and get a report:

* `python -m pybugscan --files=<filename or glob expression>`

For more options see:
 
* `python -m pybugscan -h`

## Example

```
> python -m pybugscan --files=test\test_data\dumbness.py
Mutable default arguments in file: test\test_data\dumbness.py
                Mutable default argument in func (line 4): empty list
                Mutable default argument in func (line 4): list with 2 elements
                Mutable default argument in func (line 4): empty dict
                Mutable default argument in func (line 4): dict with 1 element
                Mutable default argument in func (line 4): empty set
                Mutable default argument in func (line 4): empty set
                Mutable default argument in func (line 4): list comprehension
                Mutable default argument in func (line 4): dict comprehension
                Mutable default argument in func (line 4): set comprehension
                Mutable default argument in func (line 4): generator expression

=========================
Found the following bugs:
=========================
         - Mutable default arguments: Default arguments are created at the same time as the function, and will always refer to the same instance. See https://docs.python-guide.org/writing/gotchas/
```

## Extending to catch new bugs

Bug scanners are subclasses of `ast.NodeVisitor` from the standard lib.

1. Add a new Python file in the `pybugscan` directory
1. Add a `from pybugscan.core import BugScanner`
1. Create a subclass of `BugScanner`
1. Write the `ast.NodeVisitor` methods that you need. When you find a bug, add a description to `self.warnings`.
1. Add `from pybugscan.<new module> import <AnalyzerClass>` to `__init__.py` in the `pybugscan` directory
1. Run `python -m pybugscan` against some code with the bug and check that it gets picked up.
1. Make sure you wrote tests for it
