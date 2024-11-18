class CouplingAnalyzer:
    def __init__(self, log_data):
        self.log_data = log_data
        self.inputs_components = {}
        self.outputs_component = {}
        self.components_not_used_vars = {}
        self.inputs_related_components_outputs = {}
        self.inputs_related_sut_outputs = {}
        self.couplings = {}
        self.couplings_executions = {}
        self.coupling_id = 1
        self.individual_coupling_exercises = []
        self.dc_cc_coverarge = 0
        self.couplings_individually_exercised = 0
        self.couplings_individually_exercised_affected_sut = 0
        self.test_results = {
            'tests_failed': []
        }

    def identify_couplings_exercised(self):
        self._process_log_data()
        self._generate_couplings()
        self._set_couplings_sut_outputs_related()
        self._analyze_couplings_execution()
        self._analyze_individual_coupling_exercises_component_level()
        self._determine_dc_cc_coverage()
        self._analyse_test_result()
        return {
                'couplings': self.couplings, 'individual_coupling_exercises': self.individual_coupling_exercises, 'dc_cc_coverage': self.dc_cc_coverage, 
                'couplings_individually_exercised':self.couplings_individually_exercised, 
                'couplings_individually_exercised_affected_sut': self.couplings_individually_exercised_affected_sut,
                'test_results': self.test_results
                }

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
            if(input_key not in self.components_not_used_vars):
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
                
        for not_used in analyse['not_used']:
            if not_used not in self.inputs_components:
                self.inputs_components[not_used] = set()
            self.inputs_components[not_used].add(analyse['function'])
            
            if not_used not in self.components_not_used_vars:
                self.components_not_used_vars[not_used] = set()                
            self.components_not_used_vars[not_used].add(analyse['function'])
            
            if not_used not in self.inputs_related_components_outputs:
                self.inputs_related_components_outputs[not_used] = set()
            for output_component in analyse['out'].keys():
                self.inputs_related_components_outputs[not_used].add(output_component)

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
                filtered_outputs = (
                list(filter(lambda i: i != component_output, input_related_components_outputs))
                if input_related_components_outputs is not None
                else None
                )
                if filtered_outputs:
                    self._identify_input_related_sut_output(input_key, filtered_outputs)

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
                    if(input_component != output_component):
                        self.couplings[self.coupling_id] = {
                            "id": self.coupling_id,
                            "var": input_key,
                            "output_component": output_component,
                            "input_component": input_component,
                            # 'sut_outputs_related': list(self.inputs_related_sut_outputs.get(input_key, []))
                            'sut_outputs_related': set(),
                            'component_outputs_related': set(),
                            'found_all_suto_related': False,
                            'suts_outputs_affected': set()
                        }
                        self.coupling_id += 1
                    
    def _set_couplings_sut_outputs_related(self):
        couplings_yet_to_found_more_sut_outputs_related = set(self.couplings.keys())

        while couplings_yet_to_found_more_sut_outputs_related:
            coupling_id = couplings_yet_to_found_more_sut_outputs_related.pop()
            coupling = self.couplings[coupling_id]
            component_to_check_outputs = coupling['input_component']
            
            if(coupling['var'] in self.components_not_used_vars.keys()):
                if(component_to_check_outputs in self.components_not_used_vars.get(coupling['var'])):
                    self.couplings[coupling_id]['found_all_suto_related'] = True
                    continue
                
            
            # Obtém os outputs do componente em `outputs_component`
            outputs_from_component = [
            output for output, components in self.outputs_component.items() if component_to_check_outputs in components
            ]

            # Itera sobre cada output do componente para verificar e definir os SUT outputs relacionados
            for output_from_component in outputs_from_component:
                # Verifica se o output atual faz parte dos outputs do SUT
                if output_from_component in self.log_data['outputs']:
                    # Adiciona o output ao conjunto de `sut_outputs_related` do coupling
                    coupling['sut_outputs_related'].add(output_from_component)
                else:
                    if output_from_component in self.inputs_related_components_outputs.get(coupling['var']):
                        coupling['component_outputs_related'].add(output_from_component)
                        
            if not(coupling['component_outputs_related']):
                    self.couplings[coupling_id]['found_all_suto_related'] = True
                        
            for output_from_component in outputs_from_component:
                    # Procura couplings onde `var` é igual a `output_from_component`
                    matching_couplings = [
                        (matching_coupling_id, matching_coupling)
                        for matching_coupling_id, matching_coupling in self.couplings.items()
                        if matching_coupling['var'] == output_from_component
                    ]

                    for matching_coupling_id, matching_coupling in matching_couplings:
                        self.couplings[coupling_id]['found_all_suto_related'] = matching_coupling['found_all_suto_related']
                        # Se já existem SUT outputs relacionados neste matching_coupling, adiciona-os ao atual
                        if matching_coupling['sut_outputs_related']:
                            for sut_output_related in matching_coupling['sut_outputs_related']:
                                coupling['sut_outputs_related'].add(sut_output_related)
                        elif matching_coupling['found_all_suto_related']:
                            break
                        else:
                            # Caso algum matching_coupling ainda não tenha SUT outputs relacionados, atualiza a flag
                            self.couplings[coupling_id]['found_all_suto_related'] = False
                            couplings_yet_to_found_more_sut_outputs_related.add(coupling_id)
                            break  # Sai do loop, pois ainda falta algum SUT output relacionado

                # Remove o coupling atual do conjunto se todos os outputs relacionados foram encontrados
            if not self.couplings[coupling_id]['found_all_suto_related']:
                couplings_yet_to_found_more_sut_outputs_related.add(coupling_id)

    def _analyze_couplings_execution(self):
        for id, coupling in self.couplings.items():
            if(coupling['input_component'] not in (self.components_not_used_vars.get(coupling['var']) or [])):
                for id_log_data_executions, execution in enumerate(self.log_data['executions']):
                    component_analyse = next(
                        (analyse_item for analyse_item in execution['analysis']
                        if analyse_item['function'] == coupling['input_component']), None)
                    
                    if component_analyse:
                        self._update_coupling_execution(id, coupling, component_analyse, execution, id_log_data_executions)
            else:
                coupling['unused_var'] = True

    def _update_coupling_execution(self, id, coupling, component_analyse, execution, id_log_data_executions):
        component_inputs_values = list(component_analyse['in'].values())
        if id not in self.couplings_executions:
            component_inputs = list(component_analyse['in'].keys())
            self.couplings_executions[id] = {
                'var': coupling['var'],
                'params': component_inputs,
                'sut_outputs_related': coupling['sut_outputs_related'],
                'component_outputs_related': coupling['component_outputs_related'],
                'input_component': coupling['input_component'],
                'output_component': coupling['output_component'],
                'executions': []
            }

        component_execution = {'component_inputs_values': component_inputs_values, 'sut_values': [], 'component_outputs_related_values':[],'id_log_data_executions': id_log_data_executions}
        for sut_output_related in coupling['sut_outputs_related']:
            if sut_output_related in self.log_data['outputs']:
                suto_index = self.log_data['outputs'].index(sut_output_related)
                component_execution['sut_values'].append(execution['actualResult'][suto_index])
        
        [analyse_outputs_related_values] = [
            analyse for analyse in execution['analysis'] 
            if analyse['function'] == coupling['input_component']
        ]
        
        for component_output_related in coupling['component_outputs_related']:
            if component_output_related in analyse_outputs_related_values['out'].keys():
                component_execution['component_outputs_related_values'].append(analyse_outputs_related_values['out'].get(component_output_related))

        # component_execution.append()

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
            'sut_values': execution['sut_values'],
            'component_outputs_related_values': execution['component_outputs_related_values'],
            'id_log_data_executions': execution['id_log_data_executions']
        })
        
    def _check_outputs_suts_could_be_affected(self, values_executions, coupling_executions):
        suts_outputs_could_be_affected = {key: True for key in coupling_executions['sut_outputs_related']}
        for component_output_related in coupling_executions['component_outputs_related']:
            for sut_output_component_output_related in self.inputs_related_sut_outputs.get(component_output_related,[]):
                if sut_output_component_output_related not in self.inputs_related_components_outputs.get(coupling_executions['var']):
                    suts_outputs_could_be_affected[sut_output_component_output_related] = False
        
        for i in range(len(values_executions) - 1):
            current_component_outputs_related_values = values_executions[i]['component_outputs_related_values']
            next_component_outputs_related_values = values_executions[i + 1]['component_outputs_related_values']
            
            for index in range(len(current_component_outputs_related_values)):
                if current_component_outputs_related_values[index] != next_component_outputs_related_values[index]:
                    component_output_related = list(coupling_executions['component_outputs_related'])[index]
                    for sut_output_related in self.inputs_related_sut_outputs.get(component_output_related,[]):
                        suts_outputs_could_be_affected[sut_output_related] = True
        return suts_outputs_could_be_affected
    
    def _check_outputs_suts_affected(self, values_executions, suts_outputs_could_be_affected, coupling_executions):
        suts_outputs_affected = {key: False for key in suts_outputs_could_be_affected.keys()}
        for i in range(len(values_executions) - 1):
            current_sut_values = values_executions[i]['sut_values']
            next_sut_values = values_executions[i + 1]['sut_values']
            
            for index in range(len(current_sut_values)):
                if current_sut_values[index] != next_sut_values[index]:
                    sut_output = list(coupling_executions['sut_outputs_related'])[index]
                    if (suts_outputs_could_be_affected.get(sut_output)):
                        suts_outputs_affected[sut_output] = True
        return suts_outputs_affected
    
    def _adjusted_index(self,index):
        adjusted = 0
        for i in range(index + 1):
                while adjusted in self.log_data['skipedlines']:
                    adjusted += 1
                adjusted += 1
        return adjusted
    
    def _determine_test_vector_pair_lines(self, pair_values_execution):
        value_execution_index = self._adjusted_index(pair_values_execution[0]['id_log_data_executions'])
        other_value_execution_index = self._adjusted_index(pair_values_execution[1]['id_log_data_executions'])

        return (value_execution_index, other_value_execution_index)

    def _set_individual_coupling_exercises(self, id, non_varying_params_values_executions, non_varying_params):
        for non_varying_params_values, values_executions in non_varying_params_values_executions.items():
            if len(values_executions) > 1:
                for i, value_execution in enumerate(values_executions):
                    for j in range(i + 1, len(values_executions)):
                        pair_values_execution = [value_execution, values_executions[j]]
                        if(value_execution['var_value'] != values_executions[j]['var_value']):
                            suts_outputs_could_be_affected = self._check_outputs_suts_could_be_affected(pair_values_execution, self.couplings_executions[id])
                            suts_outputs_affected = self._check_outputs_suts_affected(pair_values_execution, suts_outputs_could_be_affected, self.couplings_executions[id])
                            self.individual_coupling_exercises.append({
                                    'id': id, 
                                    'var': self.couplings[id]['var'], 
                                    'test_vector_pair_lines': tuple(self._determine_test_vector_pair_lines(pair_values_execution)),
                                    'output_component': self.couplings[id]['output_component'],
                                    'input_component': self.couplings[id]['input_component'],
                                    'non_varying_params': list(non_varying_params.keys()),
                                    'non_varying_params_values': list(non_varying_params_values),
                                    'sut_outputs_related': self.couplings_executions[id]['sut_outputs_related'],
                                    'values_executions': pair_values_execution,
                                    'suts_outputs_could_be_affected': suts_outputs_could_be_affected,
                                    'suts_outputs_affected': suts_outputs_affected,
                                    'sut_output_affected': False
                                    })

                        
    def _check_sut_affected(self, exercise, coupling):
        sut_affected = False
        for sut_output_affected_key, sut_output_affected_value in exercise['suts_outputs_affected'].items():
            if sut_output_affected_value: 
                sut_affected = True
                coupling['suts_outputs_affected'].add(sut_output_affected_key)
        return sut_affected
    
    def _determine_dc_cc_coverage(self):
        self.dc_cc_coverage = 0
        self.couplings_individually_exercised = 0
        self.couplings_individually_exercised_affected_sut = 0
        
        # Itera sobre cada acoplamento na estrutura `couplings`
        for id, coupling in self.couplings.items():
            # Filtra exercícios individuais que correspondem ao ID do acoplamento atual
            individual_exercises = [
                exercise for exercise in self.individual_coupling_exercises
                if exercise['id'] == id
            ]
            
            if (len(individual_exercises) > 0):
                self.couplings_individually_exercised += 1
            
            # Conta quantos desses exercícios afetam a saída
            for exercise in individual_exercises:
                sut_output_affected = self._check_sut_affected(exercise, coupling)
                exercise['sut_output_affected'] = sut_output_affected

            for exercise in individual_exercises:
                if exercise['sut_output_affected']:
                    self.couplings_individually_exercised_affected_sut += 1
                    break
        
        self.dc_cc_coverage = self.couplings_individually_exercised_affected_sut / (len(self.couplings))
        
    def _analyse_test_result(self):
        self.test_results['total_tests'] = self.log_data['numberOfTests']
        self.test_results['total_tests_passed'] = len([passed for passed in self.log_data['executions'] if passed['pass'] == 'true'])
        self.test_results['total_tests_failed'] = len([failed for failed in self.log_data['executions'] if failed['pass'] == 'false'])
        for index, failed in enumerate(self.log_data['executions']):
            if failed['pass'] == 'false':
                self.test_results['tests_failed'].append({'expected_result': failed['expectedResult'], 'actual_result': failed['actualResult'], 'vector_line': self._adjusted_index(index)})