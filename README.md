Alterações em relação a Main:

V3:
- instrument_code.py atualizado, mas não utilizado nessa versão. Os testes estão utilizando o SUT original
- ⁠Bloco run_test_drive.py adicionado
- Opções para compilação (gcc e clang) (clang não testado)
- ⁠Test_Drive_Creator agora adiciona a função de contar o tempo de execução médio em microsegundos (Considera o Wall time, roda em Linux e Windows, falhas em testes pequenos e acurácia não testada)
- ⁠Nome das funções criadas não são mais variáveis 
- ⁠adicionado “if __name__ == ‘__main__’:” nos blocos

V4:
- Integração com instrument_code.py. O test_driver agora teste corretamente o SUT instrumentado
- ⁠Test_Drive_Creator agora é mais genérico, funciona com qualquer tipo de entrada ou saida, com a condição de que os ponteiros indicam as saidas
- Bloco Parser.py adicionado
    - ParseInputOutputs retorna um lista com os tipos dos parametros da função analizada
    - gerar_arquivo_h_com_pycparser gera o arquivo instrumented_SUT.h

V5: 
- Salvamento do log de execucao em um buffer 
    - Somente no goal_instrumented_SUT.c e goal_Test_Driver.c
    - goal_instrumented_SUT.c e goal_Test_Driver.c já interagem entre si
    - Tamanho do buffer ainda pequeno (ainda necessario definir um bom tamanho para o buffer) 
    - instrument_code.py e Test_Driver_Creator.y ainda não geram os goal_
- funcoes_extras.py criado para funcoes auxiliares no Test_Driver_Creator (talvez juntar com o Parser.py)
- Inicio da criação de mensagens de erro do Test_Driver_Creator.y

V6: 
- Pequenas alterações

V7:
- Integração completa entre Teste_Driver_Creator.py e instrument_code.py
- Teste_Driver_Creator.py agora identifica e e não utiliza as linhas do vetor de teste que não tem o seu tipo correspondente
- Funcao ParseNameInputsOutputs adicionada no Parser.py
- Funcao skip_lines atualizada no funcoes_extras.py (ainda não juntado com o Parser.py)
- Log de execucao no formato JSON
- Informacoes do log de execucao:
    - Nome da funcao
    - Numero de testes realizados
    - Linhas do vetor de teste não utilizadas
    - Nomes das variaveis de entrada da funcao
    - Nomes das variaveis de saida da funcao
    - Execucao dos testes:
          - Numero do teste
          - Nome dos componentes
          - Ordem de execucao
          - Nomes das variaveis de entrada dos componentes
          - Nomes das variaveis de saida dos componentes
          - Resultado do teste unitario
          - Resultados obtidos e esperados (caso o teste não passe)
          - Tempo de execucao
