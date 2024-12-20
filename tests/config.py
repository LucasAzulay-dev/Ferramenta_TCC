# Config output messages and file paths.

MSG_INSTRUMENTATION_START = "Starting code instrumentation..."
MSG_INSTRUMENTATION_END = "Instrumentation completed."
MSG_HEADER_CREATING = "Generating .h file with pycparser..."
MSG_HEADER_CREATED = ".h file generated successfully."
MSG_DRIVER_CREATING = "Creating Test Driver..."
MSG_DRIVER_CREATED = "Test Driver created successfully."
MSG_DRIVER_EXECUTING = "Running Test Driver..."

ERROR_NO_VALID_LINES = "ERROR: No valid lines in the Test Vector"
ERROR_SUT_FCN_NOT_FOUND = "ERROR: function 'wrong_name' not found."
ERROR_SUT_NO_PARAMETERS = "ERROR: function 'SUT' has no parameters."
ERROR_EXEC_ERROR = "ERROR: TestDrive not executed properly. Execution error"
ERROR_SUT_WRONG_TYPE = "ERROR: SUT is not a C file"
ERROR_TESTVEC_WRONG_TYPE = "ERROR: TestVector is not a xls or xlsx file"
ERROR_TESTVEC_MISSING_COL = "ERROR: Test vector does not have a size equivalent to the desired function. SUT columns: 9 Test_vec columns: 8"
ERROR_LOG_BUFFER_TOO_SHORT = "ERROR: TestDrive not executed properly. Execution error" 
ERROR_SUT_NO_OUTPUTS = "ERROR: No outputs detected" 
ERROR_SUT_NO_INPUTS = "ERROR: No inputs detected" 
ERROR_SUT_COMPILATION_ERROR = "ERROR: TestDrive not executed properly. Compilation error." 
ERROR_SUT_INSTRUMENTATION_ERROR = "ERROR: Instrumentation not executed properly." 
ERROR_COMPILER_NOT_ACCEPTED = "ERROR: Compiler must be gcc or clang" 

PATH_PROJ_OUTPUT = "output"
PATH_INSTRUMENTED_SUT_C = "output\\InstrumentedSUT\\instrumented_SUT.c"
PATH_INSTRUMENTED_SUT_H = "output\\InstrumentedSUT\\instrumented_SUT.h"
PATH_TEST_DRIVER_C = "output\\InstrumentedSUT\\Test_Driver.c"
PATH_TEST_DRIVER_EXE = "output\\TestDriver\\Test_Driver.exe"
PATH_LOG_BUFFER = "output\\OutputBuffer\\log_buffer.txt"
PATH_REPORT_PDF = "output\\Report\\dc_cc_analysis_report.pdf"
PATH_DIAGRAM_PDF = "output\\Report\\diagram.pdf"

PATH_FUNC_TEST_CASES = "tests\\test_cases\\functional_cases"
PATH_ROBS_TEST_CASES = "tests\\test_cases\\robustness_cases"