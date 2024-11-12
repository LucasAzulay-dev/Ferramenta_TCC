from Teste_Driver_Creator import Create_Test_Driver
from instrument_code import Create_Instrumented_Code
from run_test_drive import Run_Test_Driver
from dc_cc import DC_CC_Report_Generator
from utils import adicionar_ao_log

def executar_ferramenta(excel_file_path, code_path, function_name, folder_path ,compiler): 
    Create_Instrumented_Code(folder_path, code_path)

    log_buffer_path = "output/OutputBuffer/log_buffer.txt"
    error = Create_Test_Driver(excel_file_path, function_name, code_path, folder_path, log_buffer_path)  #FI5 parcialmente coberto

    if(error):  
        adicionar_ao_log(error)
        return
    
    adicionar_ao_log("Test Driver created successfully.")
    
    Run_Test_Driver(folder_path, code_path, compiler)
    
    adicionar_ao_log("Generating DC/CC report...")
    

    DC_CC_Report_Generator(log_buffer_path)  # Retorna os caminhos dos PDFs

# if __name__ == '__main__':

#     # Defina o caminho para o arquivo Excel
#     excel_file_path = "examples/C_proj_mockup/TestInputs/new_testvec1.xlsx"

#     # Defina o nome do arquivo .c do SUT
#     code_path = "examples/C_proj_mockup/SUT/SUT2.c" 

#     # Defina o nome da função testada
#     function_name = "SUT"

#     #Tipo de compilador
#     compiler = "gcc"    #gcc ou clang

#     executar_ferramenta(excel_file_path, code_path, function_name, compiler)
