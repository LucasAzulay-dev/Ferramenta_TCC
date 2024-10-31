import json

def analyze_static_structure(data):
    sut_outputs = data['outputs']
    sut_couplings = []
    couplings_tree = {}
    couplings_per_outputs = {output: [] for output in sut_outputs}
    coupling_id = 1
    
    # Identificar os acoplamentos
    for execution in data["executions"]:
        prev_outs = {}
        
        for step in execution["analysis"]:
            comp_name = step["function"]
            in_vars = step["in"]
            out_vars = step["out"]
            
            # Verifica acoplamentos
            for out_var, value in out_vars.items():
                prev_outs[out_var] = comp_name
            
            for in_var, value in in_vars.items():
                if in_var in prev_outs:
                    coupling = {
                        "couplingId": coupling_id,
                        "components": [prev_outs[in_var], comp_name],
                        "var": in_var
                    }
                    sut_couplings.append(coupling)
                    
                    # Atualiza a árvore de acoplamentos
                    if prev_outs[in_var] not in couplings_tree:
                        couplings_tree[prev_outs[in_var]] = {}
                    couplings_tree[prev_outs[in_var]][comp_name] = in_var
                    
                    # Atualiza acoplamentos por saída
                    for output in sut_outputs:
                        if output in out_vars:
                            couplings_per_outputs[output].append(coupling_id)
                    
                    coupling_id += 1
                    
    return {
        "sutOutputs": sut_outputs,
        "sutCouplings": sut_couplings,
        "couplingsTree": couplings_tree,
        "couplingsPerOutputs": couplings_per_outputs
    }


def dc_cc_analysis_generator(data):
    result = analyze_static_structure(data)
    print(json.dumps(result, indent=2))
