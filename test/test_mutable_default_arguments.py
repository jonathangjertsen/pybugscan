from pybugscan import mutable_default_arguments

def test_mutable_default_arguments(source_file):
    """Run the mutable default argument finder against the source and check its output"""
    source = source_file("dumbness.py")
    ana = mutable_default_arguments.MutableDefaultArgumentFinder({'possibly_mutable': True})
    ana.visit_file(source)
    warnings = ana.get_and_clear_warnings()
    assert warnings == [
        "Mutable default argument in func (line 4): empty list",
        "Mutable default argument in func (line 4): list with 2 elements",
        "Mutable default argument in func (line 4): empty dict",
        "Mutable default argument in func (line 4): dict with 1 element",
        "Mutable default argument in func (line 4): empty set",
        "Mutable default argument in func (line 4): empty set",
        "Possibly mutable default argument in func (line 4): variable 'x' in outer scope",
        "Possibly mutable default argument in func (line 4): function call",
        "Mutable default argument in func (line 4): list comprehension",
        "Mutable default argument in func (line 4): dict comprehension",
        "Mutable default argument in func (line 4): set comprehension",
        "Mutable default argument in func (line 4): generator expression",
    ]
