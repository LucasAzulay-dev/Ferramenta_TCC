import json
import re
from dc_cc_diagram import diagram_generator
#from dc_cc_analysis import CouplingAnalyzer



def corrigir_virgulas(conteudo):
    return re.sub(r',(\s*[\}\]])', r'\1', conteudo)

def DC_CC_Report_Generator(log_data):
    with open('log_buffer.txt', 'r') as file:
        conteudo = corrigir_virgulas(file.read())
        log_data = json.loads(conteudo)
        #path para arquivo pdf
        path = diagram_generator(log_data)
        #analyzer = CouplingAnalyzer(log_data)
        #path para arquivo pdf
        #analyzer.identify_couplings_exercised()
    

