import json
import re
from graphviz import Digraph
from collections import defaultdict


def corrigir_virgulas(conteudo):
    return re.sub(r',(\s*[\}\]])', r'\1', conteudo)

def gerar_diagrama(log_data):
    dot = Digraph(comment="Estrutura Observada do SUT")
    dot.attr(compound='true')  # Permite clusters

    # Cluster para o SUT com borda clara
    with dot.subgraph(name="cluster_SUT") as c:
        c.attr(label="SUT")
        c.attr(style="dashed")  # Contorno do SUT
        
        # Contadores de chamadas entre componentes e para variáveis de acoplamento
        chamadas = defaultdict(int)
        acoplamentos = defaultdict(int)  # Armazena as variáveis de acoplamento entre componentes

        # Iterar por execuções para acumular as ligações e identificar variáveis de acoplamento
        for execution in log_data["executions"]:
            for analysis in execution["analysis"]:
                component = analysis["function"]
                c.node(component, component, shape="box")

                # Registrar ligações de entradas para componentes
                for input_var in analysis["in"]:
                    chamadas[(input_var, component)] += 1

                # Registrar saídas de componentes que são usadas em outros componentes (acoplamentos)
                for output_var, next_analysis in zip(analysis["out"], execution["analysis"][1:]):
                    next_component = next_analysis["function"]
                    acoplamentos[(component, next_component, output_var)] += 1

    # Adicionar nós de entradas e saídas fora do cluster SUT
    for input_var in log_data["inputs"]:
        dot.node(input_var, input_var, shape="ellipse")
    for output_var in log_data["outputs"]:
        dot.node(output_var, output_var, shape="ellipse")

    # Criar arestas únicas com variáveis de acoplamento destacadas e dentro do SUT
    for (source, target, acoplamento_var), count in acoplamentos.items():
        # Nó de acoplamento destacado entre componentes
        with dot.subgraph(name="cluster_SUT") as c:
            c.node(acoplamento_var, acoplamento_var, shape="diamond", style="filled", color="lightblue")
            c.edge(source, acoplamento_var, label=f"Calls: {count}")
            c.edge(acoplamento_var, target)

    # Criar arestas entre entradas e componentes, e entre componentes e saídas do SUT
    for (source, target), count in chamadas.items():
        if count > 1:
            dot.edge(source, target, label=f"Calls: {count}")
        else:
            dot.edge(source, target)

    # Renderizar e exibir o diagrama
    dot.render("estrutura_sut", format="png")
    dot.view()

    
def analisar_log(log_data):
    report = {
        "totalTests": log_data["numberOfTests"],
        "tests": [],
        "uncovered_conditions": [],
        "unexecuted_components": [],
        "couplings": [],
        "dependent_outputs": []
    }

    for execution in log_data["executions"]:
        test_result = {
            "testNumber": execution["testNumber"],
            "pass": execution["pass"],
            "expectedResult": execution["expectedResult"],
            "actualResult": execution["actualResult"],
            "failed_conditions": [],
            "unexecuted_components": [],
            "coupling_info": []
        }
        
        for analysis in execution["analysis"]:
            # Exemplo de análise de acoplamento e condição
            component = analysis["function"]
            inputs = analysis["in"]
            outputs = analysis["out"]
            
            # Lógica de análise de cobertura DC/CC, acoplamentos, etc.
            # Exemplo: verificar se cada entrada foi testada individualmente
            
            test_result["coupling_info"].append({
                "component": component,
                "inputs": inputs,
                "outputs": outputs
            })

        report["tests"].append(test_result)
        
    return report

with open('log_buffer.txt', 'r') as file:
    conteudo = corrigir_virgulas(file.read())
    log_data = json.loads(conteudo)
    cobertura_report = analisar_log(log_data)
    gerar_diagrama(log_data)

print(cobertura_report)
