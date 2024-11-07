import pytest
import os
import builtins
from pathlib import Path
import shutil
import tempfile

# No meu computador (gabriel) só tá funcionando com isso
os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin\\'

# Path to example code and test vectors
sut_path_success = str(Path('examples\\C_proj_mockup\\SUT\\SUT.c').absolute())
sut_name_success = 'SUT'
testvec_success = str(Path('examples\\C_proj_mockup\\TestInputs\\new_testvec3.xlsx').absolute())
testvec_invalid_line = str(Path('examples\\C_proj_mockup\\TestInputs\\new_testvec4.xlsx').absolute())

# Path to 

class ToolParameters():
    def __init__(self, sut_path, sut_name, testvec, compiler):
        self.sut_path = sut_path
        self.sut_name = sut_name
        self.testvec = testvec
        self.compiler = compiler

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
        if os.path.isfile(file):
            os.remove(file)

# Setup: backup the 'output' directory
# Teardown: restore the original 'output' directory
@pytest.fixture(scope="session", autouse=True)
def prepare_output_directory():
    output_dir = str(Path("output").absolute())
    backup_dir = 'output_backup'

    print("Backing up output dir")    
    temp_dir = tempfile.mkdtemp()
    shutil.copytree(output_dir, os.path.join(temp_dir, backup_dir))
    for root, _, files in os.walk(output_dir):
        for file in files:
            os.remove(os.path.join(root, file))
    
    yield

    print('Restoring output dir')
    shutil.rmtree(output_dir)
    shutil.copytree(os.path.join(temp_dir, backup_dir), output_dir)
    shutil.rmtree(temp_dir)

# Pause the test, for manual checks
@pytest.fixture
def pause_test(pytestconfig):
    capmanager = pytestconfig.pluginmanager.getplugin('capturemanager')

    capmanager.suspend_global_capture(in_=True)
    input('Test paused. Press enter to resume.')
    yield

# Get parameters for success tests
@pytest.fixture
def param_success():
    param = ToolParameters(sut_path=sut_path_success,
                           sut_name=sut_name_success,
                           testvec=testvec_success,
                           compiler='gcc')
    yield param

