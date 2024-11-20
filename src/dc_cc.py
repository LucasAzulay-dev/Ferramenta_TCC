import os
import platform
import json
import re
from dc_cc_diagram import diagram_generator
from dc_cc_analysis import CouplingAnalyzer
from dc_cc_report import create_report
from utils import adicionar_ao_log

def corrigir_virgulas(conteudo):
    return re.sub(r',(\s*[\}\]])', r'\1', conteudo)

def DC_CC_Report_Generator(log_buffer_path):
    with open(log_buffer_path, 'r') as file:
        conteudo = corrigir_virgulas(file.read())
        log_data = json.loads(conteudo)

        adicionar_ao_log("Generating SUT Diagram")
        diagram_directory = 'output/Report/'
        diagram_filename = 'diagram'
        diagram_generator(log_data, diagram_directory, diagram_filename)
        path_diagram = diagram_directory + diagram_filename + '.pdf'
        adicionar_ao_log("SUT Diagram sucessfully generated")
        
        analyzer = CouplingAnalyzer(log_data)
        data = analyzer.identify_couplings_exercised()
        path_report = 'output\Report\dc_cc_analysis_report.pdf'
        create_report(data, path_report)
        return [path_diagram, path_report]