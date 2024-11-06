import pandas as pd

# Função para mapear o tipo de dados do Python para tipos de variáveis em C
def mapear_tipo_c(valor,tipo_c):
    if tipo_c == "int":
        if ((isinstance(valor, int)) and (-2147483648 <= valor <= 2147483647)):
            return 0
        else:
            return 1
    elif tipo_c == "unsigned int":
        if (isinstance(valor, int) and (0 <= valor <= 4294967295)):
            return 0  
        else:
            return 1      
    elif tipo_c == "short":
        if (isinstance(valor, int) and (-32768 <= valor <=  32767)):
            return 0
        else:
            return 1 
    elif tipo_c == "unsigned short":
        if (isinstance(valor, int) and (0 <= valor <= 65535)):
            return 0
        else:
            return 1 
    elif tipo_c == "long":
        if (isinstance(valor, int) and (-9223372036854775808 <= valor <= 9223372036854775807)):
            return 0
        else:
            return 1 
    elif tipo_c == "unsigned long":
        if (isinstance(valor, int) and (0 <= valor <= 18446744073709551615)):
            return 0
        else:
            return 1 
    elif tipo_c == "char":
        if (isinstance(valor, int) and (-128 <= valor <= 127)):
            return 0 
        else:
            return 1 
    elif tipo_c == "unsigned char":
        if (isinstance(valor, int) and (0 <= valor <= 255)):
            return 0
        else:
            return 1  
    elif tipo_c == "float":
        if (isinstance(valor, float) and (1.2E-38 <= valor <= 3.4E+38)):
            return 0 
        else:
            return 1 
    elif tipo_c == "double":
        if (isinstance(valor, float) and (2.3E-308 <= valor <= 1.7E+308)):
            return 0 
        else:
            return 1 
    elif tipo_c == "char*":
        if (isinstance(valor, str)):
            return 0 
        else:
            return 1 
    else:
        return 1  # Caso o tipo seja algo não mapeável facilmente

# Função para identificar linhas que não correspondem ao tipo especificado em uma coluna
def skip_lines(arquivo_excel, numero_coluna, tipo_c):
    # Lê o arquivo Excel

    columns_to_skip = ['Time', 'INPUT_COMMENTS', 'OUTPUT_COMMENTS']
    used_cols = lambda x: x not in columns_to_skip

    df = pd.read_excel(arquivo_excel, header = 1, usecols=used_cols, dtype=object)
    
    # Verifica se o número da coluna é válido
    if numero_coluna < 0 or numero_coluna >= len(df.columns):
        print("Número de coluna inválido.")
        return []
    
    # Pega o nome da coluna pelo índice
    nome_coluna = df.columns[numero_coluna]
    
    # Identifica linhas onde o tipo não corresponde ao especificado
    linhas_inconsistentes = []
    for indice, valor in enumerate(df[nome_coluna]):
        if (mapear_tipo_c(valor,tipo_c) == 1):
            linhas_inconsistentes.append(indice + 2)  # +2 para ajustar o índice para o usuário
    
    return linhas_inconsistentes


if __name__ == '__main__':
    # Exemplo de uso
    arquivo_excel = 'testvec5.xlsx'
    numero_coluna = 4  # Número da coluna, começando em 0
    tipo_c = 'int'     # Tipo C desejado (ex: 'int', 'float', 'char', 'string')

    linhas_inconsistentes = skip_lines(arquivo_excel, numero_coluna, tipo_c)

    if linhas_inconsistentes:
        print(f"As seguintes linhas da coluna {numero_coluna + 1} não são do tipo '{tipo_c}': {linhas_inconsistentes}")
    else:
        print(f"Todas as linhas da coluna {numero_coluna + 1} são do tipo '{tipo_c}'.")
