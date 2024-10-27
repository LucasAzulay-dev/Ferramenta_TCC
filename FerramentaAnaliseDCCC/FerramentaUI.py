#-------------------------------------------------------------------------
# FerramentaUI
# 
# Serve de interface para a ferramenta de análise DCCC.
# 
# Argumentos:
# Opção da ferramenta (Instrumentador I ou Relatório R)
# Caminho para arquivo (Arquivo C para instrumentação ou log em txt para relatório)
# 
# Uso:
# Instrumentador: python FerramentaUI I caminho_para_arquivo_c
# Relatorio: python FerramentaUI R caminho_para_arquivo_txt
#-------------------------------------------------------------------------
import sys
from Instrumentador import *

if __name__=="__main__":
    if len(sys.argv) > 2:
        opcaoFerramenta = sys.argv[1]
        filePath = sys.argv[2]
    else:
        opcaoFerramenta = 'I'
        filePath = '..\\ProjetoMockup\\src\\IntegrationFunction\\IntegrationFunction.c'

    if opcaoFerramenta == 'I':
        parse_test(filePath)