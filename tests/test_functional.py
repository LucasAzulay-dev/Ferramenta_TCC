import pytest
from .config import *
from src.Ferramenta_TCC import executar_ferramenta
from .conftest import ToolParameters, ROBUSTNESS_CASES, FUNCTIONAL_CASES, FunctionalTestConfig
import os.path


# FI#1: The Tool must accept a SUT, the name of the function to be tested, a test suite and a compiler name as input.
class TestFI_1:
    # The required inputs are accepted. Using GCC compiler
    def test_1(self, execute_functional_case):
        pass
        
# FI#2: The Tool must generate a Test Driver based on its inputs
class TestFI_2:
    def test_1(self, case_path, execute_functional_case):
        assert os.path.exists(os.path.join(case_path,PATH_TEST_DRIVER_C)) and os.path.exists(os.path.join(case_path,PATH_TEST_DRIVER_EXE))

# FI#3: The Tool must generate instrumented code from the SUT.
class TestFI_3:
    def test_1(self, case_path, execute_functional_case):        
        assert os.path.exists(os.path.join(case_path,PATH_INSTRUMENTED_SUT_C))

# FI#4: The Test Driver must execute tests using the instrumented code.
class TestFI_4:
    pass

# FI#6: The Test Driver must generate an execution log of the tests performed on the instrumented code.
class TestFI_6:
    def test_1(self, case_path, execute_functional_case):
        assert os.path.exists(os.path.join(case_path, PATH_LOG_BUFFER))

# FI#7: The execution log must indicate whether each test passed or failed.
class TestFI_7:
    # check if property 'pass' exists
    def test_1(self, get_log_json, execute_functional_case):
        json_out = get_log_json()
        assert all(execution.get("pass") in ["true", "false"] for execution in json_out.get("executions", []))

    # check if result is as expected
    def test_2(self, get_log_json, oracle_tests_passed, execute_functional_case):
        json_out = get_log_json()
        actual_tests_passed = [execution.get("pass") for execution in json_out.get("executions", [])]
        assert actual_tests_passed == oracle_tests_passed

# FI#8: The execution log must indicate which components were executed, in an ordered manner.
class TestFI_8:
    def test_1(self, get_log_json, oracle_functions_called_ordered, execute_functional_case):
        json_out = get_log_json()
        total_executions = len(json_out.get("executions",[]))
        actual_functions_called_ordered = [
            analysis.get("function")
            for execution in json_out.get("executions", [])
            for analysis in execution.get("analysis",[])
        ]
        # Assuming that the execution order is the same for all executions
        assert actual_functions_called_ordered == oracle_functions_called_ordered * total_executions

# FI#9: The execution log must report the input variables and their respective values for component execution (CC/DC).
class TestFI_9:
    pass

# FI#10: The execution log must report variables whose values may change due to each component’s execution and their values after execution.
class TestFI_10:
    pass

# FI#11: The Tool must identify variables that are simultaneously input and output parameters between components.
class TestFI_11:
    pass
