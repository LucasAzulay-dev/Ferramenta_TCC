import pandas as pd
from Parser import ParseInputOutputs, ParseNameInputsOutputs
from funcoes_extras import skip_lines
from utils import adicionar_ao_log

c_type_to_printf = {
    'int': '%d',
    'unsigned int': '%u',
    'short': '%hd',
    'unsigned short': '%hu',
    'long': '%ld',
    'unsigned long': '%lu',
    'float': '%f',
    'double': '%lf',
    'char': '%c',
    'unsigned char': '%c',
    'void': '%p',   # para ponteiros
    'char*': '%s',  # strings
}

# Criar Test_Driver
def Create_Test_Driver(excel_file_path, function_name, code_path):
    adicionar_ao_log("Criando Test Driver...")

    #Parse da quantidade de inputs e outputs, e seus tipos 
    resultado = ParseInputOutputs(code_path, function_name)
    print(resultado)

    if(isinstance(resultado, str)):
        return resultado

    #Definindo o numero de colunas do SUT
    num_colunas = resultado[0]+resultado[1]

    #Sistema para pular e printar as linhas que são incongruentes
    skipedlines = []
    for i in range(0,((num_colunas)*2),2):
        linhas_inconsistentes = skip_lines(excel_file_path, (i//2), resultado[i+3])
        skipedlines = list(set(skipedlines + linhas_inconsistentes))

    columns_to_skip = ['Time', 'INPUT_COMMENTS', 'OUTPUT_COMMENTS']
    used_cols = lambda x: x not in columns_to_skip
    #used_cols = range(1, len(pd.read_excel(excel_file_path).columns))

    # Leia o arquivo Excel
    df = pd.read_excel(excel_file_path,header=1, engine='openpyxl', usecols=used_cols, dtype=object, skiprows=skipedlines)

    num_linhas = len(df.index)    

    #Print da mensagem de erro
    if(num_linhas <= 0):
        error = f"ERROR: No valid lines in the Test Vector"
        return error

    #Definindo o numero de colunas do Test_Vec
    num_colunas_test_vec = df.shape[1]

    #Print da mensagem de erro
    if(resultado[0] <= 0):
        error = f"ERROR: No inputs detected"
        return error
    
    #Print da mensagem de erro
    if(resultado[1] <= 0):
        error = f"ERROR: No outputs detected"
        return error

    #Print da mensagem de erro
    if(num_colunas != num_colunas_test_vec):
        error = f"ERROR: Test vector does not have a size equivalent to the desired function. SUT columns: {num_colunas} Test_vec columns: {num_colunas_test_vec}"
        return error

    fromparserinputs, fromparseroutputs = ParseNameInputsOutputs(code_path, function_name)

    inicioJSON = r'  snprintf(log_buffer + strlen(log_buffer),BUFFER_SIZE - strlen(log_buffer),"{\"sutFunction\": \"' + f'{function_name}' + r'\",\"numberOfTests\": '+f'{num_linhas}'+r',  \"skipedlines\":'+f'{skipedlines}'+r',\"inputs\":'+ f'{fromparserinputs}' + r',\"outputs\": ' + f'{fromparseroutputs}'+ r',\"executions\": [");'
    fimJSON = r'  snprintf(log_buffer + strlen(log_buffer),BUFFER_SIZE - strlen(log_buffer),"],}"); '+'\n'+r'  printf("%s", log_buffer);'+'\n'

    #Definicao das strings
    param_tests_def = ""
    param_tests = ""
    param_SUT = ""
    param_outputs = ""
    return_output = ""
    test_vecs = ""
    test_outputs = ""
    print_test_outputs = ""
    print_outputs = ""
    print_outputs_types = ""
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
            test_vecs = test_vecs + '  '+resultado[i+3] + ' ' + 'test_vecs_SUTI' + f'{inputs}' + f'[{num_linhas}] =' + ' {'
            coluna_string = ', '.join(map(str, coluna.dropna().tolist()))
            test_vecs = test_vecs + coluna_string + '};\n'
            
            #Para print da função SUT
            param_SUT = param_SUT + ' SUTI' + f'{inputs},'

            inputs = inputs+1

        elif(resultado[i+2] == 'O' or resultado[i+2] == 'OR'): #se for saida ponteiros
            #Para print da função testeX
            param_tests_def = param_tests_def + ', '  + resultado[i+3] + ' ' + 'SUTO' + f'{outputs}_test' 

            #Para print dos parametros da função testeX
            param_tests = param_tests + ' test_vecs_SUTO' + f'{outputs}[i],' 

            #Para print dos test_inputs
            numero_coluna = i//2
            coluna = df.iloc[:, numero_coluna]
            test_vecs = test_vecs + '  '+resultado[i+3] + ' ' + 'test_vecs_SUTO' + f'{outputs}' + f'[{num_linhas}] =' + ' {'
            coluna_string = ', '.join(map(str, coluna.dropna().tolist()))
            test_vecs = test_vecs + coluna_string + '};\n'     

            if(resultado[i+2] == 'O'):
                #Para print da função SUT
                param_SUT = param_SUT + ' &SUTO' + f'{outputs},'
            else:
                #Para receber o return do SUT
                return_output = 'SUTO' + f'{outputs}'+' = '
             

            #Para definicoes dos outputs     
            param_outputs = param_outputs + resultado[i+3] + ' ' + 'SUTO' + f'{outputs};\n    ' 

            #Para verificacao dos testes
            test_outputs = test_outputs + ' SUTO' + f'{outputs} == SUTO' + f'{outputs}_test &&' 

            #Para print dos tipos de saida
            type_output = c_type_to_printf.get(resultado[i+3])
            if (len(print_outputs_types) == 0):
                print_outputs_types = print_outputs_types + type_output
            else:
                print_outputs_types = print_outputs_types + ',' + type_output

            #Para print da verificação dos testes
            print_test_outputs = print_test_outputs + ', SUTO' + f'{outputs}_test' 

            #Para print da verificação dos testes
            print_outputs = print_outputs + ', SUTO' + f'{outputs}' 

            outputs = outputs+1


    # Apagar resultados antigos
    testdriver_path = f'output/InstrumentedSUT/Test_Driver.c'
    open(testdriver_path, 'w').close()

    #Começar a escrever no arquivo
    with open(testdriver_path, 'a') as file:
        file.write('#include "'+ 'instrumented_SUT.h' + '"\n#include <stdio.h>\n#include <sys/time.h>\n#include <string.h>\n\n#define BUFFER_SIZE 4096\nchar log_buffer[BUFFER_SIZE];\n\nvoid testeX(int num_teste'+ param_tests_def +');\nint main(){\n  struct timeval begin, end;\n')

    #Escrever os vetores de teste de cada parametro
    with open(testdriver_path, 'a') as file:
        file.write(test_vecs)

    #Escrever os prints
    print_JSON_begin_loop = r'        snprintf(log_buffer + strlen(log_buffer),BUFFER_SIZE - strlen(log_buffer),"{\"testNumber\":%d,\"analysis\": [",i+1);'
    print_JSON_end_loop = r'        snprintf(log_buffer + strlen(log_buffer),BUFFER_SIZE - strlen(log_buffer),"\"executionTime\": %d},",elapsed);'

    #Escrever a variaveis do testeX
    with open(testdriver_path, 'a') as file:
        file.write(inicioJSON+'\n    for(int i=0;i<'+ f'{num_linhas}' +';i++){\n    '+print_JSON_begin_loop+'\n         gettimeofday(&begin,NULL);\n      testeX(i,' + param_tests)

    #Apagar "," do ultimo dado 
    with open(testdriver_path, 'rb+') as file:
        file.seek(-1, 2)
        file.truncate()

    #Print para adicionar o log em um txt
    print_create_log = r'  FILE *arquivo = fopen("output/OutputBuffer/log_buffer.txt", "w");' +'\n'+ r'  fputs(log_buffer, arquivo);'+'\n'+ r'  fputs("\n\n", arquivo);' +'\n'+ r'  fclose(arquivo);'

    #Escrever a medicao do tempo de execucao
    with open(testdriver_path, 'a') as file:
        file.write(');\n        gettimeofday(&end,NULL);\n          int elapsed = (((end.tv_sec - begin.tv_sec) * 1000000) + (end.tv_usec - begin.tv_usec))/'+ f'{num_linhas}' +';\n '+ print_JSON_end_loop +'\n     }\n'+fimJSON+print_create_log+'\nreturn 0;\n}')    

    #Escrever a definicao da funcao testeX
    with open(testdriver_path, 'a') as file:
        file.write('\nvoid testeX(int num_teste' + param_tests_def + '){\n')

    #Escrever as definições das saídas
    with open(testdriver_path, 'a') as file:
            file.write('    '+param_outputs)

    #Escrever a funcao SUT
    with open(testdriver_path, 'a') as file:
        file.write(return_output+function_name+'('+param_SUT)

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
    print_string_passed = r'   snprintf(log_buffer + strlen(log_buffer), BUFFER_SIZE - strlen(log_buffer), "],\"pass\": \"true\",");'
    print_string_failed = r'   snprintf(log_buffer + strlen(log_buffer), BUFFER_SIZE - strlen(log_buffer), "],\"pass\": \"false\",\"expectedResult\": [' + print_outputs_types + r'],\"actualResult\": [' + print_outputs_types + r'],"' + print_test_outputs + print_outputs + r');'

    with open(testdriver_path, 'a') as file:
        file.write('){\n    '+ print_string_passed+'\n      }else{\n'+print_string_failed+'\n     }\n')

    with open(testdriver_path, 'a') as file:
        file.write('}')
    #-----------------------------------------------------------------

    return 0

if __name__ == '__main__':
    # Defina o caminho para o arquivo Excel
    excel_file_path = "examples/C_proj_mockup/TestInputs/new_testvec3.xlsx"

    # Defina o nome da função testada
    function_name = "SUT"

    # Defina o nome do arquivo .c do SUT
    code_path = "examples/C_proj_mockup/SUT/SUT.c" 

    Create_Test_Driver(excel_file_path, function_name, code_path)
        