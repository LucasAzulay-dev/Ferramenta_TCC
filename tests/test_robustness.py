import pytest
from .config import *
from src.Ferramenta_TCC import executar_ferramenta
from .conftest import ToolParameters, ROBUSTNESS_CASES, FUNCTIONAL_CASES, FunctionalTestConfig
import os.path

# FI#5: The Test Driver must be able to identify and flag invalid or unexpected 
# test inputs without compromising the execution of subsequent tests.
class TestFI_5:
    # On success, no skipped tests
    def test_1(self, get_log_json, execute_functional_case):
        json_out = get_log_json()
        assert json_out['skipedlines'] == []

    # With some faulty tests, some are skipped but execution has no errors
    def test_2(self, execute_robust_case, get_log_json):
        robustness_case = 'testvec_invalid_line'
        execute_robust_case(robustness_case)
        json_out = get_log_json(robustness_case)
        assert json_out['skipedlines'] != []

    # all lines are invalid in testvec
    def test_3(self, execute_robust_case):
        robustness_case = 'testvec_all_invalid_lines'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_NO_VALID_LINES
    
    # SUT function not found
    def test_4(self, execute_robust_case):
        robustness_case = 'sut_function_not_found'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_SUT_FCN_NOT_FOUND
    
    # SUT not testable
    def test_5(self, execute_robust_case):
        robustness_case = 'sut_not_testable'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_SUT_NOT_TESTABLE

    # SUT with runtime error
    def test_6(self, execute_robust_case):
        robustness_case = 'sut_runtime_error'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_EXEC_ERROR
    
    # SUT is not a C file
    def test_7(self, execute_robust_case):
        robustness_case = 'sut_wrong_type'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_SUT_WRONG_TYPE
    
    # Tesvec is not an excel file
    def test_8(self, execute_robust_case):
        robustness_case = 'testvec_wrong_type'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_TESTVEC_WRONG_TYPE
    
    # Tesvec is missing columns
    def test_9(self, execute_robust_case):
        robustness_case = 'testvec_missing_column'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_TESTVEC_MISSING_COL
            
    # log buffer is just 1 byte long
    def test_10(self, execute_robust_case):
        robustness_case = 'log_buffer_load_error'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_LOG_BUFFER_LOAD_ERROR
