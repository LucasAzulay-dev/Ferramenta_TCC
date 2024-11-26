import pytest
from .config import *

class TestFI_5:
    """
    FI#5: The Test Driver must be capable of identifying and signaling invalid or unexpected test inputs without compromising the execution of subsequent tests.
    """
    def test_1(self, get_log_json, execute_functional_case):
        """
        TI#5.1: Verify that no tests are skipped in a correct test vector.
        """
        json_out = get_log_json()
        assert json_out['skipedlines'] == []

    def test_2(self, execute_robust_case, get_log_json):
        """
        TI#5.2: Verify that invalid test vector lines are skipped but all others are executed.
        """
        robustness_case = 'testvec_invalid_line'
        execute_robust_case(robustness_case)
        json_out = get_log_json(robustness_case)
        assert json_out['skipedlines'] == [2, 3] and json_out['numberOfTests'] == '2'

    def test_3(self, execute_robust_case):
        """
        TI#5.3: Verify that an error will be raised if all test vector lines are invalid.
        """
        robustness_case = 'testvec_all_invalid_lines'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_NO_VALID_LINES
    
    def test_4(self, execute_robust_case):
        """
        TI#5.4: Verify that an error will be raised if the informed SUT function name is not in the informed SUT file.
        """
        robustness_case = 'sut_function_not_found'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_SUT_FCN_NOT_FOUND
    
    def test_5(self, execute_robust_case):
        """
        TI#5.5: Verify that an error will be raised if the SUT function has no parameters.
        """
        robustness_case = 'sut_no_parameters'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_SUT_NO_PARAMETERS

    def test_6(self, execute_robust_case):
        """
        TI#5.6: Verify that an error will be raised if a failure occurs in the execution of the test driver.
        """
        robustness_case = 'sut_runtime_error'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_EXEC_ERROR
    
    def test_7(self, execute_robust_case):
        """
        TI#5.7: Verify that an error will be raised if the SUT is not a C file.
        """
        robustness_case = 'sut_wrong_type'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_SUT_WRONG_TYPE
    
    def test_8(self, execute_robust_case):
        """
        TI#5.8: Verify that an error will be raised if the test vector is not a xls or xlsx file.
        """
        robustness_case = 'testvec_wrong_type'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_TESTVEC_WRONG_TYPE
    
    def test_9(self, execute_robust_case):
        """
        TI#5.9: Verify that an error will be raised if the number of columns of the test vector is less than expected.
        """
        robustness_case = 'testvec_missing_column'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_TESTVEC_MISSING_COL
            
    def test_10(self, execute_robust_case):
        """
        TI#5.10: Verify that an error will be raised if the log buffer is too short for the test procedure.
        """
        robustness_case = 'log_buffer_too_short'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_LOG_BUFFER_TOO_SHORT
            
    def test_11(self, execute_robust_case):
        """
        TI#5.11: Verify that an error will be raised if the SUT function has no outputs.
        """
        robustness_case = 'sut_no_outputs'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_SUT_NO_OUTPUTS
            
    def test_12(self, execute_robust_case):
        """
        TI#5.12: Verify that an error will be raised if the SUT function has no inputs.
        """
        robustness_case = 'sut_no_inputs'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_SUT_NO_INPUTS
    
    def test_13(self, execute_robust_case):
        """
        TI#5.13: Verify that an error will be raised if the SUT function presents compilation errors.
        """
        robustness_case = 'sut_compilation_error'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value).startswith(ERROR_SUT_COMPILATION_ERROR)
    
    def test_14(self, execute_robust_case):
        """
        TI#5.14: Verify that an error will be raised if instrumentation can not be properly concluded.
        """
        robustness_case = 'sut_instrumentation_error'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_SUT_INSTRUMENTATION_ERROR

    def test_15(self, execute_robust_case):
        """
        TI#5.15: Verify that an error will be raised if an invalid compiler option is used.
        """
        robustness_case = 'compiler_wrong_name'
        with pytest.raises(Exception) as exception:
            execute_robust_case(robustness_case)
        assert str(exception.value) == ERROR_COMPILER_NOT_ACCEPTED