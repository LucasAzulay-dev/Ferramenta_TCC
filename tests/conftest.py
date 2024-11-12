import pytest
import os
import builtins
from pathlib import Path
import shutil
import tempfile
import re
import json
from .config import *

# Add graphviz to path, if installed in default folder
graphvizPathWin = os.pathsep + 'C:\\Program Files\\Graphviz\\bin\\'
if os.path.exists(graphvizPathWin):
    os.environ["PATH"] += graphvizPathWin

num_cases = 2
CASES = [f"case{i}" for i in range(1, num_cases+1)]

# Custom exception to pass tests earlier
class TestPassedException(Exception):
    pass

# Get path to all test cases
class TestPaths:
    def __init__(self, case):
        if case == 'case1':
            self.get_case_1()
        if case == 'case2':
            self.get_case_2()
    
    def get_case_1(self):
        self.sut_path = str(Path('tests\\test_cases\\case1\\src\\SUT\\SUT.c').absolute())
        self.sut_name = 'SUT'
        self.testvec_success = str(Path('tests\\test_cases\\case1\\testInputs\\success_testvec.xlsx').absolute())
        self.testvec_invalid_line = str(Path('tests\\test_cases\\case1\\testInputs\\invalid_line_testvec.xlsx').absolute())

    def get_case_2(self):
        self.sut_path = str(Path('tests\\test_cases\\case2\\src\\SUT\\SUT.c').absolute())
        self.sut_name = 'SUT'
        self.testvec_success = str(Path('tests\\test_cases\\case2\\testInputs\\success_testvec.xlsx').absolute())
        self.testvec_invalid_line = str(Path('tests\\test_cases\\case2\\testInputs\\invalid_line_testvec.xlsx').absolute())

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
    # tear-down

# Assert console output is equal to expected message
@pytest.fixture
def assert_output(capfd):
    def check_output(expected_message):
        out,_ = capfd.readouterr()
        if expected_message in out:
            raise TestPassedException()
    return check_output

# Hook to pass test when TestPassedException is raised
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if call.excinfo is not None and call.excinfo.errisinstance(TestPassedException):
        rep.outcome = "passed"

# Get JSON outputted to terminal
@pytest.fixture
def get_json(capfd):
    def get_json_output():
        out, _ = capfd.readouterr()
        

        driver_executing_msg_position = out.find(MSG_DRIVER_EXECUTING)
        if driver_executing_msg_position == -1:
            pytest.fail(f"Message of driver execution not found.")

        text_post_driver_execution = out[driver_executing_msg_position + len(MSG_DRIVER_EXECUTING):]
        
        # Usa expressão regular para identificar o JSON (assumindo que começa com '{' e termina com '}')
        json_match = re.search(r'{.*}', text_post_driver_execution, re.DOTALL)
        if json_match:
            json_text = json_match.group(0)

            # Remove commas before '}' or ']'
            json_text = re.sub(r',\s*([\}\]])', r'\1', json_text)

            try:
                json_data = json.loads(json_text)
                return json_data
            except json.JSONDecodeError:
                pytest.fail("Failed to decode JSON: "+json_text)
        else:
            pytest.fail("No JSON found.")
    
    return get_json_output

# Run tests considering all test cases
@pytest.fixture(params=CASES)
def caseConfig(request):
    return TestPaths(request.param)

# Get parameters for success tests
@pytest.fixture
def param_success(caseConfig):
    param = ToolParameters(sut_path=caseConfig.sut_path,
                           sut_name=caseConfig.sut_name,
                           testvec=caseConfig.testvec_success,
                           compiler='gcc')
    yield param

# Get parameters for tests with faulty lines in the test driver
@pytest.fixture
def param_invalid_line(caseConfig):
    param = ToolParameters(sut_path=caseConfig.sut_path,
                           sut_name=caseConfig.sut_name,
                           testvec=caseConfig.testvec_invalid_line,
                           compiler='gcc')
    yield param

