import pytest
from src.Ferramenta_TCC import executar_ferramenta
from .conftest import ToolParameters
import os.path


# FR#1: The Tool must analyze one or more execution logs of the Test Driver on the instrumented code.
class TestFR_1:
    pass

# FR#2: The Tool must generate a coverage report from the execution log results.
class TestFR_2:
    pass

# FR#3: The coverage report must indicate the DC/CC coverage of the test suite on the SUT.
class TestFR_3:
    pass

# FR#4: The coverage report must show the individual result of each test, comparing expected and actual results and indicating if the test passed or failed.
class TestFR_4:
    pass

# FR#5: The coverage report must indicate which criterion conditions were not covered.
class TestFR_5:
    pass

# FR#6: The coverage report must indicate which components were not executed.
class TestFR_6:
    pass

# FR#7: The coverage report must indicate which components have coupling and their respective coupling variables in the SUT.
class TestFR_7:
    pass

# FR#8: The coverage report must indicate which outputs of the SUT depend on each coupling.
class TestFR_8:
    pass

# FR#9: The coverage report must indicate if each component's coupling variables were varied individually with respect to other inputs.
class TestFR_9:
    pass

# FR#10: The coverage report must indicate if the observed individual variations in coupled components influenced their respective outputs in the SUT.
class TestFR_10:
    pass

# FR#11: The coverage report must indicate errors that occurred during tests executed by the Test Driver.
class TestFR_11:
    pass

# FR#12: The Tool must be able to identify and flag invalid or unexpected inputs for the Tool, halting the Tool’s execution and providing error messages.
class TestFR_12:
    pass

