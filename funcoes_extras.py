import pandas as pd

# Função para mapear o tipo de dados do Python para tipos de variáveis em C
def mapear_tipo_c(valor):
    if pd.isna(valor):
        return 'NULL'  # Representa valores ausentes
    elif isinstance(valor, int):
        return 'int'
    elif isinstance(valor, float):
        return 'float'
    elif isinstance(valor, str):
        if len(valor) == 1:
            return 'char'
        else:
            return 'string'
    else:
        return 'undefined'  # Caso o tipo seja algo não mapeável facilmente

# Função para identificar linhas que não correspondem ao tipo especificado em uma coluna
def skip_lines(arquivo_excel, numero_coluna, tipo_c):
    # Lê o arquivo Excel
    df = pd.read_excel(arquivo_excel)
    
    # Verifica se o número da coluna é válido
    if numero_coluna < 0 or numero_coluna >= len(df.columns):
        print("Número de coluna inválido.")
        return []
    
    # Pega o nome da coluna pelo índice
    nome_coluna = df.columns[numero_coluna]
    
    # Identifica linhas onde o tipo não corresponde ao especificado
    linhas_inconsistentes = []
    for indice, valor in enumerate(df[nome_coluna]):
        if mapear_tipo_c(valor) != tipo_c:
            linhas_inconsistentes.append(indice + 1)  # +1 para ajustar o índice para o usuário
    
    return linhas_inconsistentes


if __name__ == '__main__':
    # Exemplo de uso
    arquivo_excel = 'testvec2.xlsx'
    numero_coluna = 1  # Número da coluna, começando em 0
    tipo_c = 'long'     # Tipo C desejado (ex: 'int', 'float', 'char', 'string')

    linhas_inconsistentes = skip_lines(arquivo_excel, numero_coluna, tipo_c)

    if linhas_inconsistentes:
        print(f"As seguintes linhas da coluna {numero_coluna + 1} não são do tipo '{tipo_c}': {linhas_inconsistentes}")
    else:
        print(f"Todas as linhas da coluna {numero_coluna + 1} são do tipo '{tipo_c}'.")
