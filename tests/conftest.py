import pytest
import os
import builtins
from pathlib import Path

# Patch 'open' function to track all new files
def patch_open(open_func, new_files):
    def open_patched(file, mode='r', buffering=-1, encoding=None, 
                     errors=None, newline=None, closefd=True, opener=None):
        if not os.path.isfile(file):
            new_files.append(file)
        return open_func(file, mode=mode, buffering=buffering, encoding=encoding, 
                     errors=errors, newline=newline, closefd=closefd, opener=opener)
    return open_patched

# Setup: Monkeypatch build-in 'open' function
# Teardown: delete files created by tests
@pytest.fixture(autouse=True)
def cleanup_new_files(monkeypatch):
    new_files = []
    monkeypatch.setattr(builtins, 'open', patch_open(builtins.open, new_files))
    yield
    for file in new_files:
        os.remove(file)

@pytest.fixture
def sut_1():
    sut_path = str(Path('resources\\example_1\\src\\SUT\\SUT.c').absolute())
    sut_function_name = 'SUT'

    yield sut_path, sut_function_name

@pytest.fixture
def sut_1_tv_1():
    test_vector_file = str(Path('resources\\example_1\\TestInputs\\testvec1.xlsx').absolute())
    yield test_vector_file