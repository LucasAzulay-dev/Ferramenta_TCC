from graphviz import Digraph
from collections import defaultdict

def diagram_generator(log_data):
    dot = Digraph(comment="Estrutura Observada do SUT")
    dot.attr(compound='true')  # Permite clusters

    # Cluster para o SUT com borda clara
    with dot.subgraph(name="cluster_SUT") as c:
        c.attr(label="SUT")
        c.attr(style="dashed")  # Contorno do SUT
        
        # Contadores de input_vars entre componentes e para variáveis de acoplamento
        input_vars = defaultdict(int)
        output_vars = defaultdict(int)  # Armazena as variáveis de acoplamento entre componentes

        # Iterar por execuções para acumular as ligações e identificar variáveis de acoplamento
        for execution in log_data["executions"]:
            for analysis in execution["analysis"]:
                component = analysis["function"]
                c.node(component, component, shape="box")

                # Registrar ligações de entradas para componentes
                for input_var in analysis["in"]:
                    input_vars[(input_var, component)] += 1
                    
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
                dot.edge(component, output_var, label=f"Calls: {count}")
            else:
                c.edge(component, output_var, label=f"Calls: {count}")

    # Criar arestas únicas com variáveis de acoplamento destacadas e dentro do SUT
    for (input_var, component), count in input_vars.items():
        keys = [key[0] for key in output_vars.keys()]
        # Nó de acoplamento destacado entre componentes
        with dot.subgraph(name="cluster_SUT") as c:
            if(input_var in keys):
                c.node(input_var, input_var, shape="diamond", style="filled", color="lightblue")

    # Criar arestas entre entradas e componentes, e entre componentes e saídas do SUT
    for (source, target), count in input_vars.items():
        if count > 1:
            dot.edge(source, target, label=f"Calls: {count}")
        else:
            dot.edge(source, target)

    # Renderizar o diagrama sem abrir
    dot.render("estrutura_sut", format="pdf")  # Use "pdf" ou "png" conforme a necessidade

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
            
            # Lógica de análise de cobertura DC/CC, output_vars, etc.
            # Exemplo: verificar se cada entrada foi testada individualmente
            
            test_result["coupling_info"].append({
                "component": component,
                "inputs": inputs,
                "outputs": outputs
            })

        report["tests"].append(test_result)
        
    return report