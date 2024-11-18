from Teste_Driver_Creator import Create_Test_Driver
from instrument_code import Create_Instrumented_Code
from run_test_drive import Run_Test_Driver
from dc_cc import DC_CC_Report_Generator
from utils import adicionar_ao_log, Create_output_folder
from Parser import generate_ast

def executar_ferramenta(excel_file_path, code_path, function_name, compiler, bufferLength = 33554432): 

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

if __name__ == '__main__':

    # Defina o caminho para o arquivo Excel
    excel_file_path = "examples/sut_final/TestVec.xls"

    # Defina o nome do arquivo .c do SUT
    code_path = "examples/sut_final/sut.c" 

    # Defina o nome do arquivo .c do SUT
    folder_path = "examples/sut_final" 

    # Defina o nome da função testada
    function_name = "sut"

    #Tipo de compilador
    compiler = "gcc"    #gcc ou clang

    executar_ferramenta(excel_file_path, code_path, function_name, compiler)
