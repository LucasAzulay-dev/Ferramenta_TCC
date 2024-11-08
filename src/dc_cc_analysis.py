class CouplingAnalyzer:
    def __init__(self, log_data):
        self.log_data = log_data
        self.inputs_components = {}
        self.outputs_component = {}
        self.inputs_related_components_outputs = {}
        self.inputs_related_sut_outputs = {}
        self.couplings = {}
        self.couplings_executions = {}
        self.coupling_id = 1
        self.individual_coupling_exercises = []

    def identify_couplings_exercised(self):
        self._process_log_data()
        self._generate_couplings()
        self._set_couplings_sut_outputs_related()
        self._analyze_couplings_execution()
        self._analyze_individual_coupling_exercises_component_level()
        return {'couplings': self.couplings, 'individual_coupling_exercises': self.individual_coupling_exercises}

    def _process_log_data(self):
        for execution in self.log_data['executions']:
            for analyse in execution['analysis']:
                self._process_inputs(analyse)
                self._process_outputs(analyse)

        # Convert sets to lists
        self.inputs_components = {k: list(v) for k, v in self.inputs_components.items()}
        self.outputs_component = {k: list(v) for k, v in self.outputs_component.items()}

        # Identify SUT-related outputs for each input
        for input_key, components_outputs in self.inputs_related_components_outputs.items():
            self._identify_input_related_sut_output(input_key, components_outputs)

    def _process_inputs(self, analyse):
        for input_key in analyse['in']:
            if input_key not in self.inputs_components:
                self.inputs_components[input_key] = set()
            self.inputs_components[input_key].add(analyse['function'])

            if input_key not in self.inputs_related_components_outputs:
                self.inputs_related_components_outputs[input_key] = set()
            for output_component in analyse['out'].keys():
                self.inputs_related_components_outputs[input_key].add(output_component)

    def _process_outputs(self, analyse):
        for output_key in analyse['out']:
            if output_key not in self.outputs_component:
                self.outputs_component[output_key] = set()
            self.outputs_component[output_key].add(analyse['function'])

    def _identify_input_related_sut_output(self, input_key, components_outputs):
        for component_output in components_outputs:
            if component_output in self.log_data['outputs']:
                self._set_input_related_sut_output(input_key, component_output)
            else:
                input_related_components_outputs = self.inputs_related_components_outputs.get(component_output)
                if input_related_components_outputs:
                    self._identify_input_related_sut_output(input_key, input_related_components_outputs)

    def _set_input_related_sut_output(self, input_key, component_output):
        if component_output in self.log_data['outputs']:
            if input_key not in self.inputs_related_sut_outputs:
                self.inputs_related_sut_outputs[input_key] = set()
            self.inputs_related_sut_outputs[input_key].add(component_output)

    def _generate_couplings(self):
        for input_key, input_components in self.inputs_components.items():
            output_components = self.outputs_component.get(input_key, [])
            for input_component in input_components:
                for output_component in output_components:
                    self.couplings[self.coupling_id] = {
                        "id": self.coupling_id,
                        "var": input_key,
                        "output_component": output_component,
                        "input_component": input_component,
                        # 'sut_outputs_related': list(self.inputs_related_sut_outputs.get(input_key, []))
                        'sut_outputs_related': set()
                    }
                    self.coupling_id += 1
                    
    def _set_couplings_sut_outputs_related(self):
        couplings_yet_to_found_more_sut_outputs_related = set(self.couplings.keys())

        while couplings_yet_to_found_more_sut_outputs_related:
            coupling_id = couplings_yet_to_found_more_sut_outputs_related.pop()
            coupling = self.couplings[coupling_id]
            component_to_check_outputs = coupling['input_component']
            
            # Obtém os outputs do componente em `outputs_component`
            outputs_from_component = [
            output for output, components in self.outputs_component.items() if component_to_check_outputs in components
            ]

            # Itera sobre cada output do componente para verificar e definir os SUT outputs relacionados
            for output_from_component in outputs_from_component:
                found_all = True

                # Verifica se o output atual faz parte dos outputs do SUT
                if output_from_component in self.log_data['outputs']:
                    # Adiciona o output ao conjunto de `sut_outputs_related` do coupling
                    coupling['sut_outputs_related'].add(output_from_component)
                else:
                    # Procura couplings onde `var` é igual a `output_from_component`
                    matching_couplings = [
                        (matching_coupling_id, matching_coupling)
                        for matching_coupling_id, matching_coupling in self.couplings.items()
                        if matching_coupling['var'] == output_from_component
                    ]

                    # Assume que todos foram encontrados, mas isso pode mudar ao iterar
                    found_all = False
                    
                    # Verifica cada coupling correspondente para encontrar os SUT outputs relacionados
                    for matching_coupling_id, matching_coupling in matching_couplings:
                        # Se já existem SUT outputs relacionados neste matching_coupling, adiciona-os ao atual
                        if matching_coupling['sut_outputs_related']:
                            for sut_output_related in matching_coupling['sut_outputs_related']:
                                coupling['sut_outputs_related'].add(sut_output_related)
                            found_all = True
                        else:
                            # Caso algum matching_coupling ainda não tenha SUT outputs relacionados, atualiza a flag
                            found_all = False
                            couplings_yet_to_found_more_sut_outputs_related.add(coupling_id)
                            break  # Sai do loop, pois ainda falta algum SUT output relacionado

                # Remove o coupling atual do conjunto se todos os outputs relacionados foram encontrados
                if not found_all:
                    couplings_yet_to_found_more_sut_outputs_related.add(coupling_id)

                    
    def _analyze_couplings_execution(self):
        for id, coupling in self.couplings.items():
            for execution in self.log_data['executions']:
                component_analyse = next(
                    (analyse_item for analyse_item in execution['analysis']
                     if analyse_item['function'] == coupling['input_component']), None)
                
                if component_analyse:
                    self._update_coupling_execution(id, coupling, component_analyse, execution)

    def _update_coupling_execution(self, id, coupling, component_analyse, execution):
        if id not in self.couplings_executions:
            component_inputs = list(component_analyse['in'].keys())
            component_inputs_values = list(component_analyse['in'].values())
            self.couplings_executions[id] = {
                'var': coupling['var'],
                'params': component_inputs,
                'sut_outputs_related': coupling['sut_outputs_related'],
                'executions': []
            }
        else:
            component_inputs_values = list(component_analyse['in'].values())

        component_execution = {'component_inputs_values': component_inputs_values, 'sut_values': []}
        for sut_output_related in coupling['sut_outputs_related']:
            if sut_output_related in self.log_data['outputs']:
                suto_index = self.log_data['outputs'].index(sut_output_related)
                component_execution['sut_values'].append(execution['actualResult'][suto_index])

        self.couplings_executions[id]['executions'].append(component_execution)

    def _analyze_individual_coupling_exercises_component_level(self):
        for id, coupling_executions in self.couplings_executions.items():
            non_varying_params = {}
            non_varying_params_values_executions = {}
            coupling_values_executions_index = None

            for index, param in enumerate(coupling_executions['params']):
                if param != coupling_executions['var']:
                    non_varying_params[param] = index
                else:
                    coupling_values_executions_index = index

            for execution in coupling_executions['executions']:
                self._analyze_non_varying_params(execution, non_varying_params, coupling_values_executions_index, non_varying_params_values_executions)

            self._set_individual_coupling_exercises(id, non_varying_params_values_executions, non_varying_params)

    def _analyze_non_varying_params(self, execution, non_varying_params, coupling_values_executions_index, non_varying_params_values_executions):
        non_varying_params_values_execution = [
            execution['component_inputs_values'][index]
            for index in non_varying_params.values()
        ]

        key = tuple(non_varying_params_values_execution)
        if key not in non_varying_params_values_executions:
            non_varying_params_values_executions[key] = []
        non_varying_params_values_executions[key].append({
            'var_value': execution['component_inputs_values'][coupling_values_executions_index],
            'sut_values': execution['sut_values']
        })
        
    def _check_sut_affected(self, values_executions):
        for i in range(len(values_executions) - 1):
            current_sut_values = values_executions[i]['sut_values']
            next_sut_values = values_executions[i + 1]['sut_values']
            
            for index in range(len(current_sut_values)):
                if current_sut_values[index] != next_sut_values[index]:
                    return True 
        return False

    def _set_individual_coupling_exercises(self, id, non_varying_params_values_executions, non_varying_params):
        for non_varying_params_values, values_executions in non_varying_params_values_executions.items():
            if len(values_executions) > 1:
                sut_outputs_affected = self._check_sut_affected(values_executions)
                self.individual_coupling_exercises.append({
                    'id': id, 
                    'var': self.couplings[id]['var'], 
                    'output_component': self.couplings[id]['output_component'],
                    'input_component': self.couplings[id]['input_component'],
                    'non_varying_params': list(non_varying_params.keys()),
                    'non_varying_params_values': list(non_varying_params_values),
                    'sut_outputs_related': self.couplings_executions[id]['sut_outputs_related'],
                    'values_executions': values_executions,
                    'sut_outputs_affected': sut_outputs_affected
                    })