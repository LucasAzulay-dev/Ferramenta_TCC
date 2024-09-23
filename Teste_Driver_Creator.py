import pandas as pd

# Criar Test_Driver
def Create_Test_Driver(excel_file_path, instrumented_path, function_name, num_output):

    # Leia o arquivo Excel
    df = pd.read_excel(excel_file_path, engine='openpyxl', usecols=range(1, len(pd.read_excel(excel_file_path).columns)))

    num_linhas = f'{len(df.index)}'
    num_colunas = df.shape[1]

    # Apagar resultados antigos
    testdriver_path = f'Test_Driver.c'
    open(testdriver_path, 'w').close()

    #Começar a escrever no arquivo
    with open(testdriver_path, 'a') as file:
        file.write('#include "'+ instrumented_path + '"\n#include <stdio.h>\nvoid testeX(int num_teste, int SUTI[]);\nint main(){\n   int test_inputs[' + num_linhas + f'][{num_colunas}]'+' = {\n')

    # Itere sobre as linhas do DataFrame
    for index, row in df.iterrows():                           
        
        # Converta a linha em uma string
        line_content = ','.join(str(item) for item in row.values)
        
        # Escreva o conteúdo da linha no arquivo de texto
        with open(testdriver_path, 'a') as file:
            file.write('\n        {' + line_content + '},')

    #Apagar "," do ultimo dado 
    with open(testdriver_path, 'rb+') as file:
        file.seek(-1, 2)
        file.truncate()

    with open(testdriver_path, 'a') as file:
        file.write('\n    };\n for(int i=0;i<'+ num_linhas +';i++){\n    testeX(i+1,test_inputs[i]);\n   }\n return 0;\n}')

    with open(testdriver_path, 'a') as file:
        file.write('\nvoid testeX(int num_teste, int SUTI[]){\n')

    #Escrever as definições das saídas
    for i in range(num_output):
        with open(testdriver_path, 'a') as file:
            file.write(f'    int SUTO{i+1};\n')

    with open(testdriver_path, 'a') as file:
        file.write('    '+function_name+'(')

    #Escrever as entradas
    for i in range(num_colunas - num_output):
        with open(testdriver_path, 'a') as file:
            file.write(f'SUTI[{i}], ')

    #Escrever as saídas
    for i in range(num_output):
        with open(testdriver_path, 'a') as file:
            file.write(f' &SUTO{i+1},')

    #Apagar "," do ultimo dado 
    with open(testdriver_path, 'rb+') as file:
        file.seek(-1, 2)
        file.truncate()

    with open(testdriver_path, 'a') as file:
        file.write(');\n')

    #Fazer teste unitário
    #-----------------------------------------------------------------
    with open(testdriver_path, 'a') as file:
        file.write(f'    if(')

    #Escrever as comparações das saídas do SUT com as do Vetor de Testes
    for i in range(num_output):
        with open(testdriver_path, 'a') as file:
            file.write(f' SUTO{i+1}==SUTI[{num_colunas - num_output +i}] &&')

    #Apagar "&&" do ultimo dado 
    for i in range(2):
        with open(testdriver_path, 'rb+') as file:
            file.seek(-1, 2)
            file.truncate()

    #Escrever os prints
    print_string_passed = r'   printf("Teste %d : PASSOU\n", num_teste);'
    print_string_failed = r'        printf("Teste %d: FALHOU\n", num_teste);'

    with open(testdriver_path, 'a') as file:
        file.write('){\n    '+ print_string_passed+'\n      }else{\n'+print_string_failed+'\n     }\n')
    #-----------------------------------------------------------------

    with open(testdriver_path, 'a') as file:
        file.write('}')

# Defina o caminho para o arquivo Excel
excel_file_path = "testvec1.xlsx"

# Defina o caminho para o arquivo .h do SUT instrumentado
instrumented_path = "SUT.h"

# Defina o nome da função testada
function_name = "SUT"

# Defina a quantidade de outputs
num_output = 1

Create_Test_Driver(excel_file_path, instrumented_path, function_name, num_output)
        