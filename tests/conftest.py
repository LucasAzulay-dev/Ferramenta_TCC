from .config import *
import pytest
import os
from pathlib import Path
import shutil
import tempfile
import re
import json
from .config import *
import platform
from src.Ferramenta_TCC import executar_ferramenta
from contextlib import redirect_stdout, redirect_stderr
import io

FUNCTIONAL_CASES = [
    # 'case_embraer_base',
    # 'case_embraer_changed_names',
    # 'case_embraer_tests_failed',
    # 'case1',
    # 'case_100_coverage',
    # 'case_unused_var',
    # 'case_sut_return',
    # 'case_comp_no_param',
    # 'case_separated_files',
    # 'case_unused_related_output',
    'case_pointer_assigned',
]
ROBUSTNESS_CASES = {
    'sut_function_not_found' :{
        'case_folder' : 'sut_function_not_found',
        'sut_file_name': 'SUT.c',
        'sut_fcn_name' : 'wrong_name',
        'testvec_name' : 'testvec.xlsx',
        'buffer_length' : None
    },
    'sut_not_testable' :{
        'case_folder' : 'sut_not_testable',
        'sut_file_name': 'SUT_not_testable.c',
        'sut_fcn_name' : 'SUT',
        'testvec_name' : 'testvec.xlsx',
        'buffer_length' : None
    },
    'sut_runtime_error' :{
        'case_folder' : 'sut_runtime_error',
        'sut_file_name': 'SUT_exec_error.c',
        'sut_fcn_name' : 'SUT',
        'testvec_name' : 'testvec.xlsx',
        'buffer_length' : None
    },
    'sut_wrong_type' :{
        'case_folder' : 'sut_wrong_type',
        'sut_file_name': 'SUT_wrong_type.cpp',
        'sut_fcn_name' : 'SUT',
        'testvec_name' : 'testvec.xlsx',
        'buffer_length' : None
    },
    'testvec_all_invalid_lines' :{
        'case_folder' : 'testvec_all_invalid_lines',
        'sut_file_name': 'SUT.c',
        'sut_fcn_name' : 'SUT',
        'testvec_name' : 'testvec_all_invalid_lines.xlsx',
        'buffer_length' : None
    },
    'testvec_invalid_line' :{
        'case_folder' : 'testvec_invalid_line',
        'sut_file_name': 'SUT.c',
        'sut_fcn_name' : 'SUT',
        'testvec_name' : 'testvec_invalid_line.xlsx',
        'buffer_length' : None
    },
    'testvec_missing_column' :{
        'case_folder' : 'testvec_missing_column',
        'sut_file_name': 'SUT.c',
        'sut_fcn_name' : 'SUT',
        'testvec_name' : 'testvec_missing_column.xlsx',
        'buffer_length' : None
    },
    'testvec_wrong_type' :{
        'case_folder' : 'testvec_wrong_type',
        'sut_file_name': 'SUT.c',
        'sut_fcn_name' : 'SUT',
        'testvec_name' : 'testvec_wrong_type.csv',
        'buffer_length' : None
    },
    'log_buffer_too_short' :{
        'case_folder' : 'log_buffer_too_short',
        'sut_file_name': 'sut.c',
        'sut_fcn_name' : 'sut',
        'testvec_name' : 'TestVec.xls',
        'buffer_length' : 1
    },
}

# Get path to all functional test cases
class FunctionalTestConfig:
    def __init__(self, case):
        self.case_dir = str(Path(PATH_FUNC_TEST_CASES+'\\'+case).absolute())
        self.sut_path = str(Path(PATH_FUNC_TEST_CASES+'\\'+case+'\\src\\sut.c').absolute())
        self.sut_name = 'sut'
        self.buffer_length = None
        self.testvec = str(Path(PATH_FUNC_TEST_CASES+'\\'+case+'\\testInputs\\testvec.xls').absolute())
        if not os.path.isfile(self.testvec):
            self.testvec = str(Path(PATH_FUNC_TEST_CASES+'\\'+case+'\\testInputs\\testvec.xlsx').absolute())
        # oracles
        self.oracle_tests_passed = str(Path(PATH_FUNC_TEST_CASES+'\\'+case+'\\oracle\\testsPassed.txt').absolute())
        self.oracle_functions_called_ordered = str(Path(PATH_FUNC_TEST_CASES+'\\'+case+'\\oracle\\functionsCalledOrdered.txt').absolute())
        # output
        self.case_out = str(Path(PATH_FUNC_TEST_CASES+'\\'+case+'\\'+PATH_PROJ_OUTPUT).absolute())

# Get path to all robustness test cases
class RobustnessTestConfig:
    def __init__(self, robustness_case):
        case = ROBUSTNESS_CASES[robustness_case]
        self.case_dir = str(Path(PATH_ROBS_TEST_CASES +'\\'+ case['case_folder']).absolute())
        self.sut_path = str(Path(PATH_ROBS_TEST_CASES +'\\'+ case['case_folder']+'\\'+case['sut_file_name']).absolute())
        self.sut_name = case['sut_fcn_name']
        self.buffer_length = case['buffer_length']
        self.testvec = str(Path(PATH_ROBS_TEST_CASES +'\\'+ case['case_folder']+'\\'+case['testvec_name']).absolute())
        # output
        self.case_out = str(Path(PATH_ROBS_TEST_CASES+'\\'+case['case_folder']+'\\'+PATH_PROJ_OUTPUT).absolute())
    
class ToolParameters():
    def __init__(self, sut_path, sut_name, testvec, compiler, buffer_length=None):
        self.sut_path = sut_path
        self.sut_name = sut_name
        # self.proj_dir = proj_dir
        self.testvec = testvec
        self.compiler = compiler
        self.buffer_length = buffer_length

# Setup: backup the 'output' directory
# Teardown: restore the original 'output' directory
@pytest.fixture(scope="session", autouse=True)
def prepare_output_directory():
    output_dir = str(Path("output").absolute())
    backup_dir = 'output_backup'

    print("[pytest] Backing up output dir")    
    temp_dir = tempfile.mkdtemp()
    shutil.copytree(output_dir, os.path.join(temp_dir, backup_dir))
    for root, _, files in os.walk(output_dir):
        for file in files:
            os.remove(os.path.join(root, file))
    
    yield

    print('[pytest] Restoring output dir')
    shutil.rmtree(output_dir)
    shutil.copytree(os.path.join(temp_dir, backup_dir), output_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture(scope="session")
def monkeysession():
    with pytest.MonkeyPatch.context() as mp:
        yield mp

@pytest.fixture(scope='session', params=FUNCTIONAL_CASES, autouse=False)
def execute_functional_case(request, monkeysession):
    """
    Execute and save the output of the test case
    """
    # Monkeypatch to avoid opening the pdf report
    if platform.system() == "Windows":
        monkeysession.setattr(os, "startfile", lambda path, operation=None: None)
    else:
        monkeysession.setattr(os, "system", lambda path, operation=None: None)

    case = request.param
    request.session.current_case = case #save context for other fixtures
    print("[pytest] Executing case - "+ case)
    param, paths = _get_case_config(case)
    _clean_test_output_dir(paths)
    f_out, f_err = io.StringIO(), io.StringIO()
    with redirect_stdout(f_out), redirect_stderr(f_err):
        executar_ferramenta(excel_file_path=param.testvec,  
                            code_path=param.sut_path, 
                            function_name=param.sut_name, 
                            compiler=param.compiler)
    _copy_test_output(paths)
    _saveTerminalOutput(paths, f_out.getvalue(), f_err.getvalue())

@pytest.fixture()
def execute_robust_case(monkeypatch):
    """
    Execute and save the output of robust test cases
    """
    # Monkeypatch to avoid opening the pdf report
    if platform.system() == "Windows":
        monkeypatch.setattr(os, "startfile", lambda path, operation=None: None)
    else:
        monkeypatch.setattr(os, "system", lambda path, operation=None: None)

    def run_robust_case(case):
        print("[pytest] Executing robustness case - "+ case)
        param, paths = _get_case_config(case, isRobust=True)
        _clean_test_output_dir(paths)
        f_out, f_err = io.StringIO(), io.StringIO()
        exception = None
        with redirect_stdout(f_out), redirect_stderr(f_err):
            # print("[pytest] bufferLength is None: " + param.buffer_length == None)
            try:
                if param.buffer_length == None:
                    executar_ferramenta(excel_file_path=param.testvec,  
                                        code_path=param.sut_path, 
                                        function_name=param.sut_name, 
                                        compiler=param.compiler)
                else:
                    executar_ferramenta(excel_file_path=param.testvec,  
                                        code_path=param.sut_path, 
                                        function_name=param.sut_name, 
                                        compiler=param.compiler,
                                        bufferLength=param.buffer_length)
            except Exception as e:
                exception = e
                f_err.write(str(e))
            finally:
                _copy_test_output(paths)
                _saveTerminalOutput(paths, f_out.getvalue(), f_err.getvalue())
        if exception:
            raise exception
    return run_robust_case

@pytest.fixture()
def dont_open_report(monkeypatch):
    # Monkeypatch to avoid opening the pdf report
    if platform.system() == "Windows":
        monkeypatch.setattr(os, "startfile", lambda path, operation=None: None)
    else:
        monkeypatch.setattr(os, "system", lambda path, operation=None: None)

# Get JSON outputted to terminal
@pytest.fixture()
def get_log_json(request):
    def get_log_buffer(robustness_case=''):
        if robustness_case == '':
            case = request.session.current_case
            _, paths = _get_case_config(case)
        else:
            case = robustness_case
            _, paths = _get_case_config(case, isRobust=True)
        log_buffer_txt = _getCaseLogBuffer(paths)
        json_match = re.search(r'{.*}', log_buffer_txt, re.DOTALL)
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
    return get_log_buffer

# Get oracle of tests passed
@pytest.fixture
def oracle_tests_passed(request):
    case = request.session.current_case
    _, paths = _get_case_config(case)
    return _textFileToList(paths.oracle_tests_passed)

# Get oracle of tests passed
@pytest.fixture
def oracle_functions_called_ordered(request):
    case = request.session.current_case
    _, paths = _get_case_config(case)
    return _textFileToList(paths.oracle_functions_called_ordered)

@pytest.fixture
def case_path(request):
    case = request.session.current_case
    _, paths = _get_case_config(case)
    return paths.case_dir

def _get_case_config(case, isRobust=False):
    """
    Get data related to the test case.
    Returns the parameters and the case paths.
    """
    if isRobust:
        case_config = RobustnessTestConfig(case)
    else:
        case_config = FunctionalTestConfig(case)

    if case_config.buffer_length == None:
        case_params = ToolParameters(sut_path=case_config.sut_path,
                            # proj_dir=case_config.proj_dir,
                            sut_name=case_config.sut_name,
                            testvec=case_config.testvec,
                            compiler='gcc')
    else:
        case_params = ToolParameters(sut_path=case_config.sut_path,
                            # proj_dir=case_config.proj_dir,
                            sut_name=case_config.sut_name,
                            testvec=case_config.testvec,
                            buffer_length=case_config.buffer_length,
                            compiler='gcc')
    return case_params, case_config

def _clean_test_output_dir(case_path : FunctionalTestConfig | RobustnessTestConfig):
    """
    Clean the test case output folder.
    """
    print("[pytest] Cleaning test output folder...")
    case_output_dir = Path(case_path.case_out)
    if case_output_dir.exists():
        shutil.rmtree(case_output_dir)
    case_output_dir.mkdir(parents=True)

def _copy_test_output(case_path : FunctionalTestConfig | RobustnessTestConfig):
    """
    Copy the project output folder to the test case output folder.
    """
    print("[pytest] Coping project output to case output...")
    proj_output_dir = Path(PATH_PROJ_OUTPUT)
    case_output_dir = Path(case_path.case_out)
    if proj_output_dir.exists():
        shutil.copytree(proj_output_dir, case_output_dir, dirs_exist_ok=True)

def _saveTerminalOutput(case_path : FunctionalTestConfig | RobustnessTestConfig, out, err):
    """
    Save the terminal output to files in the case output folder
    """
    out_path = os.path.join(case_path.case_out, 'terminal_out.txt')
    err_path = os.path.join(case_path.case_out, 'terminal_errors.txt')
    with open(out_path, 'w', encoding='utf-8') as file:
        file.write(out)
    with open(err_path, 'w', encoding='utf-8') as file:
        file.write(err)

def _getCaseLogBuffer(casePath: FunctionalTestConfig | RobustnessTestConfig):
    buffer_path = os.path.join(casePath.case_dir, PATH_LOG_BUFFER)
    with open(buffer_path, 'r', encoding='utf-8') as file:
        log_buffer_txt = file.read()
    return log_buffer_txt

# return the lines of a text file as a list
def _textFileToList(filePath):
    with open(filePath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = [
        line.strip() for line in lines
        if not line.startswith('#')
        ]
    return lines
