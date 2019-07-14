from pathlib import Path

import pytest

DATA_DIR = (Path(__file__).parent / "test_data")

@pytest.fixture
def source_file():
    """Returns a function that returns the path to a script in the test data directory"""
    return lambda name: (DATA_DIR / name).absolute()
