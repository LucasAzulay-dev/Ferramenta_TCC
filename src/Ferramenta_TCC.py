from Teste_Driver_Creator import Create_Test_Driver
from instrument_code import Create_Instrumented_Code
from run_test_drive import Run_Test_Driver
from dc_cc_report_generator import DC_CC_Report_Generator

from Parser import gerar_arquivo_h_com_pycparser  #Mudar para instrument_code.py

# # Defina o caminho para o arquivo Excel
# excel_file_path = "testvec2.xlsx"

# # Defina o nome do arquivo .c do SUT
# code_path = "SUT.c"

# # Defina o nome da função testada
# function_name = "SUT"

# #Tipo de compilador
# compiler = "gcc"    #gcc ou clang

def executar_ferramenta(excel_file_path, code_path, function_name, compiler):   
    Create_Instrumented_Code(code_path)

    gerar_arquivo_h_com_pycparser(code_path) #Mudar para instrument_code.py

    Create_Test_Driver(excel_file_path, function_name, code_path)  #FI5 não coberto

    Run_Test_Driver(compiler)

    DC_CC_Report_Generator("log_data")
