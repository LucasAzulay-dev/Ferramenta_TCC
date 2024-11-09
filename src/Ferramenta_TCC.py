from Teste_Driver_Creator import Create_Test_Driver
from instrument_code import Create_Instrumented_Code
from run_test_drive import Run_Test_Driver
from dc_cc_report_generator import DC_CC_Report_Generator

def executar_ferramenta(excel_file_path, code_path, function_name, compiler):   

    Create_Instrumented_Code(code_path)

    Create_Test_Driver(excel_file_path, function_name, code_path)  #FI5 não coberto

    Run_Test_Driver(compiler)

    #DC_CC_Report_Generator("log_data")

if __name__ == '__main__':

    # Defina o caminho para o arquivo Excel
    excel_file_path = "examples/C_proj_mockup/TestInputs/new_testvec1.xlsx"

    # Defina o nome do arquivo .c do SUT
    code_path = "examples/C_proj_mockup/SUT/SUT.c" 

    # Defina o nome da função testada
    function_name = "SUT"

    #Tipo de compilador
    compiler = "gcc"    #gcc ou clang

    executar_ferramenta(excel_file_path, code_path, function_name, compiler)
