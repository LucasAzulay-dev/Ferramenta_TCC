import json
import re
from dc_cc_diagram import diagram_generator
from dc_cc_analysis import dc_cc_analysis_generator



def corrigir_virgulas(conteudo):
    return re.sub(r',(\s*[\}\]])', r'\1', conteudo)

with open('log_buffer.txt', 'r') as file:
    conteudo = corrigir_virgulas(file.read())
    log_data = json.loads(conteudo)
    # diagram_generator(log_data)
    dc_cc_analysis_generator(log_data)
    

