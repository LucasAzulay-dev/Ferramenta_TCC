import os
import platform
import json
import re
from dc_cc_diagram import diagram_generator
from dc_cc_analysis import CouplingAnalyzer
from dc_cc_report import create_report

def corrigir_virgulas(conteudo):
    return re.sub(r',(\s*[\}\]])', r'\1', conteudo)

def DC_CC_Report_Generator(log_buffer_path):
    with open(log_buffer_path, 'r') as file:
        conteudo = corrigir_virgulas(file.read())
        log_data = json.loads(conteudo)
 
        path_diagram = diagram_generator(log_data)
        
        analyzer = CouplingAnalyzer(log_data)
        data = analyzer.identify_couplings_exercised()
        path_report = 'dc_cc_analysis_report.pdf'
        create_report(data, path_report)
        # if platform.system() == "Windows":
        #     os.startfile(path_report)
        # elif platform.system() == "Darwin":  # macOS
        #     os.system(f"open {path_report}")
        # else:  # Assume Linux
        #     os.system(f"xdg-open {path_report}")
        # return data