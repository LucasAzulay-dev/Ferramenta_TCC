from datetime import datetime
import os
import pandas as pd

log_widget = None  # Variável global para armazenar o widget de log

def configurar_log_widget(widget):
    global log_widget
    log_widget = widget

def adicionar_ao_log(mensagem):
    print(mensagem)
    if log_widget:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        log_widget.config(state="normal")
        start_index = log_widget.index("end-1c")  
        log_widget.insert("end", timestamp + mensagem + "\n")
        end_index = log_widget.index("end-1c") 
        log_widget.tag_add("black", start_index, end_index)
        log_widget.see("end")
        log_widget.config(state="disable")
        log_widget.update_idletasks()

def adicionar_ao_log_error(mensagem):
    print(mensagem)
    if log_widget:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        log_widget.config(state="normal")
        start_index = log_widget.index("end-1c")  
        log_widget.insert("end", timestamp + mensagem + "\n")
        end_index = log_widget.index("end-1c") 
        log_widget.tag_add("red", start_index, end_index)
        log_widget.see("end")
        log_widget.config(state="disable")
        log_widget.update_idletasks()

def Create_output_folder(base_path="output"):
    try:
        adicionar_ao_log("Creating Output folder...")
        # Define o caminho da pasta principal
        pasta_principal = os.path.join(base_path)
        
        # Lista com os nomes das subpastas
        subpastas = ["InstrumentedSUT", "TestDriver", "Report", "OutputBuffer"]
        
        # Cria a pasta principal, se não existir
        if not os.path.exists(pasta_principal):
            os.makedirs(pasta_principal)
        
        # Cria as subpastas dentro da pasta principal
        for subpasta in subpastas:
            caminho_subpasta = os.path.join(pasta_principal, subpasta)
            if not os.path.exists(caminho_subpasta):
                os.makedirs(caminho_subpasta)

        adicionar_ao_log("Output folder created successfully.")
        return 0
    except:
        error = f"ERROR: Output folder not created properly." # {e.stderr}
        raise Exception(error)
    
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
        if ((isinstance(valor, float) and (-1.2E+38 <= valor <= 3.4E+38)) or isinstance(valor, int)):
            return 0 
        else:
            return 1 
    elif tipo_c == "double":
        if ((isinstance(valor, float) and (-1.2E+38 <= valor <= 3.4E+38)) or isinstance(valor, int)):
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

    df = pd.read_excel(arquivo_excel, engine='calamine',header = 1, usecols=used_cols, dtype=object)
    
    # Verifica se o número da coluna é válido
    if numero_coluna < 0 or numero_coluna >= len(df.columns):
        return []
    
    # Pega o nome da coluna pelo índice
    nome_coluna = df.columns[numero_coluna]
    
    # Identifica linhas onde o tipo não corresponde ao especificado
    linhas_inconsistentes = []
    for indice, valor in enumerate(df[nome_coluna]):
        if (mapear_tipo_c(valor,tipo_c) == 1):
            linhas_inconsistentes.append(indice + 2)  # +2 para ajustar o índice para o usuário
    
    return linhas_inconsistentes

def list_c_files(code_path, exclude):
    caminhos_c = []  # Lista para armazenar os caminhos dos arquivos .c
    try:
        for root, dirs, files in os.walk(code_path):
            for file in files:
                if file.endswith('.c'):
                    caminho_formatado = os.path.join(root, file).replace("\\", "/")
                    # Adiciona o caminho apenas se ele não corresponder ao caminho a ser excluído
                    if caminho_formatado != exclude.replace("\\", "/"):
                        caminhos_c.append(caminho_formatado)
        
        # Junta todos os caminhos com uma vírgula como separador
        return caminhos_c
    except Exception as e:
        return ""
    
def list_c_directories(code_path, exclude):
    directories = set()  # Usamos um conjunto para evitar diretórios duplicados
    try:
        for root, dirs, files in os.walk(code_path):
            for file in files:
                if file.endswith('.c'):
                    dir_path = os.path.dirname(os.path.join(root, file)).replace("\\", "/")
                    # Adiciona o diretório apenas se ele não for o caminho a ser excluído
                    if dir_path != os.path.dirname(exclude.replace("\\", "/")):
                        directories.add('-I' + dir_path)  # Adiciona o diretório ao conjunto
        
        # Retorna a lista de diretórios com -I
        return list(directories)
    except Exception as e:
        return []
