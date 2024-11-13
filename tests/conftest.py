import pytest
import os
import builtins
from pathlib import Path
import shutil
import tempfile
import re
import json
from .config import *
import platform

FUNCTIONAL_CASES = ['case1', 'case2', 'case3']
ROBUSTNESS_CASES = {
    'sut_function_not_found' :{
        'case_folder' : 'sut_function_not_found',
        'sut_file_name': 'SUT.c',
        'sut_fcn_name' : 'SUT',
        'testvec_name' : 'testvec.xlsx'
    },
    'sut_not_testable' :{
        'case_folder' : 'sut_not_testable',
        'sut_file_name': 'SUT_not_testable.c',
        'sut_fcn_name' : 'SUT',
        'testvec_name' : 'testvec.xlsx'
    },
    'sut_runtime_error' :{
        'case_folder' : 'sut_runtime_error',
        'sut_file_name': 'SUT_exec_error.c',
        'sut_fcn_name' : 'SUT',
        'testvec_name' : 'testvec.xlsx'
    },
    'sut_wrong_type' :{
        'case_folder' : 'sut_wrong_type',
        'sut_file_name': 'SUT_wrong_type.cpp',
        'sut_fcn_name' : 'SUT',
        'testvec_name' : 'testvec.xlsx'
    },
    'testvec_all_invalid_lines' :{
        'case_folder' : 'testvec_all_invalid_lines',
        'sut_file_name': 'SUT.c',
        'sut_fcn_name' : 'SUT',
        'testvec_name' : 'testvec_all_invalid_lines.xlsx'
    },
    'testvec_invalid_line' :{
        'case_folder' : 'testvec_invalid_line',
        'sut_file_name': 'SUT.c',
        'sut_fcn_name' : 'SUT',
        'testvec_name' : 'testvec_invalid_line.xlsx'
    },
    'testvec_missing_column' :{
        'case_folder' : 'testvec_missing_column',
        'sut_file_name': 'SUT.c',
        'sut_fcn_name' : 'SUT',
        'testvec_name' : 'testvec_missing_column.xlsx'
    },
    'testvec_wrong_type' :{
        'case_folder' : 'testvec_wrong_type',
        'sut_file_name': 'SUT.c',
        'sut_fcn_name' : 'SUT',
        'testvec_name' : 'testvec_wrong_type.csv'
    },
}

# Custom exception to pass tests earlier
class TestPassedException(Exception):
    pass

# Get path to all functional test cases
class FunctionalTestPaths:
    def __init__(self, case):
        self.sut_path = str(Path('tests\\test_cases\\functional_cases\\'+case+'\\src\\SUT\\SUT.c').absolute())
        self.proj_dir = str(Path('tests\\test_cases\\functional_cases\\'+case+'\\src').absolute())
        self.sut_name = 'SUT'
        self.testvec = str(Path('tests\\test_cases\\functional_cases\\'+case+'\\testInputs\\testvec.xlsx').absolute())

# Get path to all robustness test cases
class RobustnessTestPaths:
    def __init__(self, robustness_case):
        self.sut_path = str(Path('tests\\test_cases\\robustness_cases\\'+robustness_case['case_folder']+'\\'+robustness_case['sut_file_name']).absolute())
        self.proj_dir = str(Path('tests\\test_cases\\robustness_cases\\'+robustness_case['case_folder']).absolute())
        self.sut_name = robustness_case['sut_fcn_name']
        self.testvec = str(Path('tests\\test_cases\\robustness_cases\\'+robustness_case['case_folder']+'\\'+robustness_case['testvec_name']).absolute())
    
class ToolParameters():
    def __init__(self, sut_path, sut_name, proj_dir, testvec, compiler):
        self.sut_path = sut_path
        self.sut_name = sut_name
        self.proj_dir = proj_dir
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

# Monkeypatch os.startfile or os.system to prevent the opening of the report after every execution
@pytest.fixture(autouse=True)
def dont_open_report(monkeypatch):
    def mock_startfile(path):
        pass

    def mock_system(command):
        pass

    if platform.system() == "Windows":
        monkeypatch.setattr(os, "startfile", mock_startfile)
    else:
        monkeypatch.setattr(os, "system", mock_system)

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
def get_log_json(capfd):
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

# Run tests considering all functional test cases
@pytest.fixture(params=FUNCTIONAL_CASES)
def functional_config(request):
    return FunctionalTestPaths(request.param)

# Get parameters for success tests
@pytest.fixture
def param_success(functional_config : FunctionalTestPaths):
    param = ToolParameters(sut_path=functional_config.sut_path,
                           proj_dir=functional_config.proj_dir,
                           sut_name=functional_config.sut_name,
                           testvec=functional_config.testvec,
                           compiler='gcc')
    return param

# Get parameters for tests with some faulty lines in the test driver
@pytest.fixture
def param_robustness_case():
    def get_robustness_params(robustness_case):
        rubustness_config = RobustnessTestPaths(robustness_case)
        param = ToolParameters(sut_path=rubustness_config.sut_path,
                            proj_dir=rubustness_config.proj_dir,
                            sut_name=rubustness_config.sut_name,
                            testvec=rubustness_config.testvec,
                            compiler='gcc')
        return param
    return get_robustness_params