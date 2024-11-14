from Teste_Driver_Creator import Create_Test_Driver
from instrument_code import Create_Instrumented_Code
from run_test_drive import Run_Test_Driver
from dc_cc import DC_CC_Report_Generator
from utils import adicionar_ao_log, Create_output_folder

def executar_ferramenta(excel_file_path, code_path, function_name, folder_path ,compiler, bufferLength = 33554432): 

    error_create_output_folder = Create_output_folder()

    if(error_create_output_folder):  
        adicionar_ao_log(error_create_output_folder)
        return

    error_create_instrumented_code = Create_Instrumented_Code(folder_path, code_path, function_name, bufferLength)

    if(error_create_instrumented_code):  
        adicionar_ao_log(error_create_instrumented_code)
        return

    log_buffer_path = "output/OutputBuffer/log_buffer.txt"
    error_create_testdriver = Create_Test_Driver(excel_file_path, function_name, code_path, folder_path, log_buffer_path, bufferLength)  #FI5 parcialmente coberto

    if(error_create_testdriver):  
        adicionar_ao_log(error_create_testdriver)
        return
    
    adicionar_ao_log("Test Driver created successfully.")
    
    error_run_testdriver = Run_Test_Driver(folder_path, code_path, compiler)

    if(error_run_testdriver):  
        adicionar_ao_log(error_run_testdriver)
        return
    
    adicionar_ao_log("Generating DC/CC report...")
    

    return DC_CC_Report_Generator(log_buffer_path)  # Retorna os caminhos dos PDFs

if __name__ == '__main__':

    # Defina o caminho para o arquivo Excel
    excel_file_path = "tests\\test_cases\\functional_cases\\case2\\testInputs\\testvec.xlsx"

    # Defina o nome do arquivo .c do SUT
    code_path = "tests\\test_cases\\functional_cases\\case2\\src\\SUT\\SUT.c" 

    # Defina o nome do arquivo .c do SUT
    folder_path = "tests\\test_cases\\functional_cases\\case2\\src" 

    # Defina o nome da função testada
    function_name = "SUT"

    #Tipo de compilador
    compiler = "gcc"    #gcc ou clang

    executar_ferramenta(excel_file_path, code_path, function_name, folder_path, compiler)
