import subprocess
from Teste_Driver_Creator import Create_Test_Driver
from instrument_code import Create_Intrumented_Code

# Defina o caminho para o arquivo Excel
excel_file_path = "testvec2.xlsx"

# Defina o nome do arquivo .c do SUT
code_path = "SUT.c"

Create_Intrumented_Code(code_path)

# Defina o caminho para o arquivo .c do SUT instrumentado
instrumented_c_path = "SUT.c"     #Substituir por instrumented_SUT.c

# Defina o caminho para o arquivo .h do SUT instrumentado
instrumented_h_path = "SUT.h"     #Substituir por instrumented_SUT.h

# Defina o nome da função testada
function_name = "SUT"

# Defina a quantidade de outputs
num_output = 1

Create_Test_Driver(excel_file_path, instrumented_h_path, function_name, num_output)  #FI5 não coberto

#Compila o programa C
subprocess.run(["gcc", instrumented_c_path, "Test_Driver.c", "-o", "Test_Driver"], check=True)

# Executa o programa C
subprocess.run([".\Test_Driver.exe"], check=True)