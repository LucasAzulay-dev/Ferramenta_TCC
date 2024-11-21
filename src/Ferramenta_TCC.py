from Teste_Driver_Creator import Create_Test_Driver
from instrument_code import Create_Instrumented_Code
from run_test_drive import Run_Test_Driver
from dc_cc import DC_CC_Report_Generator
from utils import adicionar_ao_log, Create_output_folder
from Parser import generate_ast

def executar_ferramenta(excel_file_path : str, code_path : str, function_name : str, compiler : str, bufferLength = 33554432): 

    if not code_path.endswith('.c'):
        raise Exception("ERROR: SUT is not a C file")

    if not (excel_file_path.endswith('.xls') or excel_file_path.endswith('.xlsx')):
        raise Exception("ERROR: TestVector is not a xls or xlsx file")
    
    if not (compiler == 'gcc' or compiler == 'clang'):
        raise Exception("ERROR: Compiler must be gcc or clang")

    Create_output_folder()

    ast = generate_ast(code_path)

    instrumented_code_path = Create_Instrumented_Code(ast, function_name, bufferLength)
    
    adicionar_ao_log("Instrumented Code created successfully.")
    

    log_buffer_path = "output/OutputBuffer/log_buffer.txt"
    test_driver_path = Create_Test_Driver(excel_file_path, function_name, ast, log_buffer_path, bufferLength)  #FI5 parcialmente coberto

    adicionar_ao_log("Test Driver created successfully.")
    
    Run_Test_Driver(instrumented_code_path, test_driver_path,compiler)

    adicionar_ao_log("Generating DC/CC report...")
    
    return DC_CC_Report_Generator(log_buffer_path)  # Retorna os caminhos dos PDFs