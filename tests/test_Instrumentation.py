import pytest
from .config import *
from src.Ferramenta_TCC import executar_ferramenta
from .conftest import ToolParameters, ROBUSTNESS_CASES
import os.path

# FI#1: The Tool must accept a SUT, the name of the function to be tested, a test suite and a compiler name as input.
class TestFI_1:
    # The required inputs are accepted. Using GCC compiler
    def test_1(self, param_success, assert_output):
        param : ToolParameters = param_success
        executar_ferramenta(excel_file_path=param.testvec, 
                            folder_path=param.proj_dir, 
                            code_path=param.sut_path, 
                            function_name=param.sut_name, 
                            compiler=param.compiler)
        assert_output(MSG_INSTRUMENTATION_START)
        
# FI#2: The Tool must generate a Test Driver based on its inputs
class TestFI_2:
    def test_1(self, param_success):
        param : ToolParameters = param_success
        executar_ferramenta(excel_file_path = param.testvec, 
                            folder_path=param.proj_dir,
                            code_path = param.sut_path, 
                            function_name = param.sut_name, 
                            compiler = param.compiler)
        
        assert os.path.exists(PATH_TEST_DRIVER_C) and os.path.exists(PATH_TEST_DRIVER_EXE)

# FI#3: The Tool must generate instrumented code from the SUT.
class TestFI_3:
    def test_1(self, param_success):
        param : ToolParameters = param_success
        executar_ferramenta(excel_file_path = param.testvec, 
                            folder_path=param.proj_dir,
                            code_path = param.sut_path, 
                            function_name = param.sut_name, 
                            compiler = param.compiler)
        
        assert os.path.exists(PATH_INSTRUMENTED_SUT_C)

# FI#4: The Test Driver must execute tests using the instrumented code.
class TestFI_4:
    pass

# FI#5: The Test Driver must be able to identify and flag invalid or unexpected 
# test inputs without compromising the execution of subsequent tests.
class TestFI_5:
    # On success, no skipped tests
    def test_1(self, param_success, get_log_json):
        param : ToolParameters = param_success
        executar_ferramenta(excel_file_path = param.testvec, 
                            folder_path=param.proj_dir,
                            code_path = param.sut_path, 
                            function_name = param.sut_name, 
                            compiler = param.compiler)
        json_out = get_log_json()
        assert json_out['skipedlines'] == []

    # With some faulty tests, some are skipped but execution has no errors
    def test_2(self, param_robustness_case, get_log_json):
        param : ToolParameters = param_robustness_case(ROBUSTNESS_CASES['testvec_invalid_line'])
        executar_ferramenta(excel_file_path = param.testvec, 
                            folder_path=param.proj_dir,
                            code_path = param.sut_path, 
                            function_name = param.sut_name, 
                            compiler = param.compiler)
        json_out = get_log_json()
        assert json_out['skipedlines'] != []

# FI#6: The Test Driver must generate an execution log of the tests performed on the instrumented code.
class TestFI_6:
    pass

# FI#7: The execution log must indicate whether each test passed or failed.
class TestFI_7:
    pass

# FI#8: The execution log must indicate which components were declared.
class TestFI_8:
    pass

# FI#9: The execution log must indicate which components were executed, in an ordered manner.
class TestFI_9:
    pass

# FI#10: The execution log must report the declared variables and their respective types (DC).
class TestFI_10:
    pass

# FI#11: The execution log must report the input variables and their respective values for component execution (CC/DC).
class TestFI_11:
    pass

# FI#12: The execution log must report variables whose values may change due to each component’s execution and their values after execution.
class TestFI_12:
    pass

# FI#13: The Tool must identify variables that are simultaneously input and output parameters between components.
class TestFI_13:
    pass
