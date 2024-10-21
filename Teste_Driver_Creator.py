import pandas as pd
from Parser import ParseInputOutputs

# Criar Test_Driver
def Create_Test_Driver(excel_file_path, function_name, code_path):

    # Leia o arquivo Excel
    df = pd.read_excel(excel_file_path, engine='openpyxl', usecols=range(1, len(pd.read_excel(excel_file_path).columns)))

    num_linhas = f'{len(df.index)}'          

    #Parse da quantidade de inputs e outputs, e seus tipos 
    resultado = ParseInputOutputs(code_path, function_name)

    #Definindo o numero de colunas
    num_colunas = resultado[0]+resultado[1]

    #Definicao das strings
    param_tests_def = ""
    param_tests = ""
    param_SUT = ""
    param_outputs = ""
    test_vecs = ""
    test_outputs = ""
    inputs = 1
    outputs = 1

    #Escrever todos os prints que dependem dos inputs e outputs
    for i in range(0,(num_colunas)*2,2):
        if(resultado[i+2] == 'I'): #Se for entrada
            #Para print da função definicao testeX
            param_tests_def = param_tests_def + ', ' + resultado[i+3] + ' ' + 'SUTI' + f'{inputs}' 

            #Para print dos parametros da função testeX
            param_tests = param_tests + ' test_vecs_SUTI' + f'{inputs}[i],' 

            #Para print dos test_inputs
            numero_coluna = i//2
            coluna = df.iloc[:, numero_coluna]
            test_vecs = test_vecs + '   '+resultado[i+3] + ' ' + 'test_vecs_SUTI' + f'{inputs}' + f'[{num_linhas}] =' + ' {'
            coluna_string = ', '.join(map(str, coluna.dropna().tolist()))
            test_vecs = test_vecs + coluna_string + '};\n'
            
            #Para print da função SUT
            param_SUT = param_SUT + ' SUTI' + f'{inputs},'

            inputs = inputs+1

        elif(resultado[i+2] == 'O'): #se for saida
            #Para print da função testeX
            param_tests_def = param_tests_def + ', '  + resultado[i+3] + ' ' + 'SUTO' + f'{outputs}_test' 

            #Para print dos parametros da função testeX
            param_tests = param_tests + ' test_vecs_SUTO' + f'{outputs}[i],' 

            #Para print dos test_inputs
            numero_coluna = i//2
            coluna = df.iloc[:, numero_coluna]
            test_vecs = test_vecs + '   '+resultado[i+3] + ' ' + 'test_vecs_SUTO' + f'{outputs}' + f'[{num_linhas}] =' + ' {'
            coluna_string = ', '.join(map(str, coluna.dropna().tolist()))
            test_vecs = test_vecs + coluna_string + '};\n'     

            #Para print da função SUT
            param_SUT = param_SUT + ' &SUTO' + f'{outputs},' 

            #Para definicoes dos outputs     
            param_outputs = param_outputs + resultado[i+3] + ' ' + 'SUTO' + f'{outputs};\n    ' 

            #Para verificacao dos testes
            test_outputs = test_outputs + ' SUTO' + f'{outputs} == SUTO' + f'{outputs}_test &&' 

            outputs = outputs+1
        else:
            print('DEFINIR ERRO')


    # Apagar resultados antigos
    testdriver_path = f'Test_Driver.c'
    open(testdriver_path, 'w').close()

    #Começar a escrever no arquivo
    with open(testdriver_path, 'a') as file:
        file.write('#include "'+ 'instrumented_SUT.h' + '"\n#include <stdio.h>\n#include <sys/time.h>\n\nvoid testeX(int num_teste'+ param_tests_def +');\nint main(){\n   struct timeval begin, end;\n')

    #Escrever os vetores de teste de cada parametro
    with open(testdriver_path, 'a') as file:
        file.write(test_vecs)

    #Escrever os prints
    print_string_execution_time = r'printf("Execution time: %d micro seconds\n",elapsed);'

    #Escrever a variaveis do testeX
    with open(testdriver_path, 'a') as file:
        file.write('\n  gettimeofday(&begin,NULL);\n    for(int i=0;i<'+ num_linhas +';i++){\n      testeX(i,' + param_tests)

    #Apagar "," do ultimo dado 
    with open(testdriver_path, 'rb+') as file:
        file.seek(-1, 2)
        file.truncate()

    #Escrever a medicao do tempo de execucao
    with open(testdriver_path, 'a') as file:
        file.write(');\n    }\n  gettimeofday(&end,NULL);\n  int elapsed = (((end.tv_sec - begin.tv_sec) * 1000000) + (end.tv_usec - begin.tv_usec))/'+ num_linhas +';\n '+ print_string_execution_time +'\n return 0;\n}')    

    #Escrever a definicao da funcao testeX
    with open(testdriver_path, 'a') as file:
        file.write('\nvoid testeX(int num_teste' + param_tests_def + '){\n')

    #Escrever as definições das saídas
    with open(testdriver_path, 'a') as file:
            file.write('    '+param_outputs)

    #Escrever a funcao SUT
    with open(testdriver_path, 'a') as file:
        file.write(function_name+'('+param_SUT)

    #Apagar "," do ultimo dado 
    with open(testdriver_path, 'rb+') as file:
        file.seek(-1, 2)
        file.truncate()

    with open(testdriver_path, 'a') as file:
        file.write(');\n')

    #Fazer teste unitário
    #-----------------------------------------------------------------
    with open(testdriver_path, 'a') as file:
        file.write(f'    if('+test_outputs)

    #Apagar "&&" do ultimo dado 
    for i in range(2):
        with open(testdriver_path, 'rb+') as file:
            file.seek(-1, 2)
            file.truncate()

    #Escrever os prints
    print_string_passed = r'   printf("Teste %d : PASSOU\n", num_teste+1);'
    print_string_failed = r'        printf("Teste %d: FALHOU\n", num_teste+1);'

    with open(testdriver_path, 'a') as file:
        file.write('){\n    '+ print_string_passed+'\n      }else{\n'+print_string_failed+'\n     }\n')
    #-----------------------------------------------------------------

    with open(testdriver_path, 'a') as file:
        file.write('}')

if __name__ == '__main__':
    # Defina o caminho para o arquivo Excel
    excel_file_path = "testvec2.xlsx"

    # Defina o nome da função testada
    function_name = "SUT"

    # Defina o nome do arquivo .c do SUT
    code_path = "SUT.c" 

    Create_Test_Driver(excel_file_path, function_name, code_path)
        