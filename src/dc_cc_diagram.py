from graphviz import Digraph
from collections import defaultdict

def diagram_generator(log_data, diagram_directory, diagram_filename):
    dot = Digraph(comment="Estrutura Observada do SUT")
    dot.attr(compound='true')  # Permite clusters

    # Cluster para o SUT com borda clara
    with dot.subgraph(name="cluster_SUT") as c:
        c.attr(label="SUT")
        c.attr(style="dashed")  # Contorno do SUT
        
        # Contadores de input_vars entre componentes e para variáveis de acoplamento
        input_vars = defaultdict(int)
        output_vars = defaultdict(int)  # Armazena as variáveis de acoplamento entre componentes
        not_used_vars = defaultdict(int)  # Armazena as variáveis de acoplamento entre componentes

        # Iterar por execuções para acumular as ligações e identificar variáveis de acoplamento
        for execution in log_data["executions"]:
            for analysis in execution["analysis"]:
                component = analysis["function"]
                c.node(component, component, shape="box")

                # Registrar ligações de entradas para componentes
                for input_var in analysis["in"]:
                    input_vars[(input_var, component)] += 1
                    
                for not_used_var in analysis["not_used"]:
                    not_used_vars[(not_used_var, component)] += 1
                    
                for output_var in analysis["out"]:
                    output_vars[(output_var, component)] += 1

    # Adicionar nós de entradas e saídas fora do cluster SUT
    for input_sut_var in log_data["inputs"]:
        dot.node(input_sut_var, input_sut_var, shape="ellipse")
    for output_sut_var in log_data["outputs"]:
        dot.node(output_sut_var, output_sut_var, shape="ellipse")

    # Criar arestas únicas com variáveis de acoplamento destacadas e dentro do SUT
    for (output_var, component), count in output_vars.items():
        keys = [key[0] for key in output_vars.keys()]
        # Nó de acoplamento destacado entre componentes
        with dot.subgraph(name="cluster_SUT") as c:
            if(output_var in log_data["outputs"]):
                dot.edge(component, output_var)
            else:
                c.edge(component, output_var)

    # Criar arestas únicas com variáveis de acoplamento destacadas e dentro do SUT
    for (input_var, component), count in input_vars.items():
        keys = [key[0] for key in output_vars.keys()]
        # Nó de acoplamento destacado entre componentes
        with dot.subgraph(name="cluster_SUT") as c:
            if(input_var in keys):
                c.node(input_var, input_var, shape="diamond", style="filled", color="lightblue")
                
    for (input_var, component), count in not_used_vars.items():
        keys = [key[0] for key in not_used_vars.keys()]
        # Nó de acoplamento NÃO UTILIZADO destacado entre componentes
        with dot.subgraph(name="cluster_SUT") as c:
            if(input_var in keys):
                c.node(input_var, input_var, shape="ellipse")

    # Criar arestas entre entradas e componentes, e entre componentes e saídas do SUT
    for (source, target), count in input_vars.items():
        input_output_var = output_vars.get((source, target))
        if input_output_var:
            with dot.subgraph(name="cluster_SUT") as c:
                c.node(source + '_input', source, shape="ellipse")
                c.edge(source + '_input', target)
        else:
            dot.edge(source, target)
            
    # Criar arestas entre entradas e componentes, e entre componentes e saídas do SUT
    for (source, target), count in not_used_vars.items():
        dot.edge(source, target, color='red', arrowhead='onormal')

    # Renderizar o diagrama sem abrir
    dot.render(diagram_filename, directory=diagram_directory, format="pdf")  # Use "pdf" ou "png" conforme a necessidade

    report = {
        "totalTests": log_data["numberOfTests"],
        "tests": [],
        "uncovered_conditions": [],
        "unexecuted_components": [],
        "couplings": [],
        "dependent_outputs": []
    }

    for execution in log_data["executions"]:
        if (execution["pass"] == 'false'):
            test_result = {
                "testNumber": execution["testNumber"],
                "pass": execution["pass"],
                "expectedResult": execution["expectedResult"],
                "actualResult": execution["actualResult"],
                "failed_conditions": [],
                "unexecuted_components": [],
                "coupling_info": []
            }
        else:
            test_result = {
                "testNumber": execution["testNumber"],
                "pass": execution["pass"],
                "failed_conditions": [],
                "unexecuted_components": [],
                "coupling_info": []
            }
        
        for analysis in execution["analysis"]:
            # Exemplo de análise de acoplamento e condição
            component = analysis["function"]
            inputs = analysis["in"]
            outputs = analysis["out"]
            
            # Lógica de análise de cobertura DC/CC, output_vars, etc.
            # Exemplo: verificar se cada entrada foi testada individualmente
            
            test_result["coupling_info"].append({
                "component": component,
                "inputs": inputs,
                "outputs": outputs
            })

        report["tests"].append(test_result)
        
    return report