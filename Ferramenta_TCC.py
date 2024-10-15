import subprocess
from Teste_Driver_Creator import Create_Test_Driver
from instrument_code import Create_Instrumented_Code
from run_test_drive import Run_Test_Driver

# Defina o caminho para o arquivo Excel
excel_file_path = "testvec1.xlsx"

# Defina o nome do arquivo .c do SUT
code_path = "SUT.c"

# Defina o nome da função testada
function_name = "SUT"

#Tipo de compilador
compiler = "gcc"    #gcc ou clang

Create_Instrumented_Code(code_path)

# Defina a quantidade de outputs
num_output = 1

Create_Test_Driver(excel_file_path, function_name, num_output)  #FI5 não coberto

Run_Test_Driver(compiler)