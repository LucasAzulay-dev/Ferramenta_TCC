from fpdf import FPDF
from utils import adicionar_ao_log

class PDF(FPDF):
    def __init__(self, data):
        super().__init__()  # Chama o construtor da classe pai
        self.data = data  # Armazena os dados de log
        self.couplings_color = {}

    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "DC/CC Analysis Report", 0, 1, "C")
        self.ln(5)  # Adiciona um espaço após o cabeçalho

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(2)

    def chapter_body(self, body):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, body)
        self.ln()
        
    def add_test_results(self):
        # Adiciona seção resultados dos testes
        self.chapter_title("Tests Results")
        test_percentage = (self.data['test_results']['total_tests_passed'])/(int)(self.data['test_results']['total_tests']) * 100
        color = (0, 128, 0) if test_percentage >= 100 else (255, 69, 0)
        adicionar_ao_log(f"Tests Passed: {test_percentage:.1f}%")
        
        tab_space = 5  # Define o valor do recuo desejado
        # Exibe a porcentagem de cobertura
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(30, 5, "Tests Passed: ", 0)
        self.set_text_color(*color)
        self.cell(0, 5, f"{test_percentage:.1f}%", 0, 1)
        self.set_text_color(0, 0, 0)
        self.ln(5)
        
        # Exibe total de testes
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(30, 5, "Total Tests: ", 0)
        self.set_font("Arial", "", 12)
        self.cell(0, 5, f"{self.data['test_results']['total_tests']}", 0, 1)
        self.set_text_color(0, 0, 0)
        self.ln(5)
        
        # Exibe total de testes falharam
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(30, 5, "Failed Tests: ", 0)
        self.set_font("Arial", "", 12)
        self.cell(0, 5, f"{self.data['test_results']['total_tests_failed']}", 0, 1)
        self.set_text_color(0, 0, 0)
        self.ln(5)
        
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        test_failed_vector_lines = []
        if(len(self.data['test_results']['tests_failed'])):
            self.cell(0, 5, "Test Failed Description:", 0, 1)
            self.set_text_color(0, 0, 0)
            for test_failed in self.data['test_results']['tests_failed']:
                self.add_resume_test_failed(test_failed)
                test_failed_vector_lines.append(test_failed['vector_line'])
            self.ln(5)
        adicionar_ao_log(f"Tests Failed (Vector Line): {','.join(map(str, test_failed_vector_lines))}")
        
    def add_resume_test_failed(self, test_failed):
        tab_space = 10
        color = (255, 69, 0)
        self.set_text_color(*color)
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(32, 10, f"- Vector Line: {test_failed['vector_line']}", 10, 1)
        self.cell(100, 10, f" Expected Result: {test_failed['expected_result']} | "+f"Actual Result: {test_failed['actual_result']}", 10, 1)
        self.set_text_color(0, 0, 0)
        
    def add_dc_cc_coverage_section(self):
        # Adiciona seção de cobertura com cores baseadas no valor
        self.chapter_title("DC/CC Coverage Summary")
        coverage_percentage = self.data['dc_cc_coverage'] * 100
        color = (0, 128, 0) if coverage_percentage > 85 else (255, 150, 0) if coverage_percentage > 50 else (255, 0, 0)
        self.set_text_color(*color)
        adicionar_ao_log(f"DC/CC Coverage: {coverage_percentage:.1f}%")
        
        tab_space = 5  # Define o valor do recuo desejado
        # Exibe a porcentagem de cobertura
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(0, 5, f"DC/CC Coverage: {coverage_percentage:.1f}%", 30, 30)
        self.set_text_color(0, 0, 0)
        self.ln(5)
        
        # Exibe total de acoplamentos identificados
        identified_coupligs = len(self.data['couplings'])
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(0, 5, f"Identified Couplings: {identified_coupligs}", 0, 1)
        self.set_text_color(0, 0, 0)
        self.ln(5)
        adicionar_ao_log(f"Identified Couplings: {identified_coupligs}")
        
        # Exibe total de acoplamento exercitados individualmente que afetaram o sut output
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(0, 5, f"Couplings Exercised Independent and Affecting Outputs: {self.data['couplings_individually_exercised_affected_sut']}", 0, 1)
        self.set_text_color(0, 0, 0)
        self.ln(5)
        adicionar_ao_log(f"Couplings Exercised Independent and Affecting Outputs: {self.data['couplings_individually_exercised_affected_sut']}")
        
        # Exibe total de acoplamento exercitados individualmente que não afetaram o sut output
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        color = (0, 128, 0) if self.data['couplings_individually_exercised'] > 0 else (0,0,0)
        self.cell(0, 5, f"Couplings Exercised Independent and Not Affecting Outputs: {self.data['couplings_individually_exercised']-self.data['couplings_individually_exercised_affected_sut']}", 0, 1)
        self.set_text_color(0, 0, 0)
        self.ln(5)
        
        # Exibe total de acoplamento exercitados individualmente que não afetaram o sut output
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(0, 5, "Coupling Variable Analysis:", 0, 1)
        self.set_text_color(0, 0, 0)
        for coupling in self.data['couplings'].values():
            self.add_resume_coupling_analysis(coupling)
        self.ln(5)
        
    def add_div(self):
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)
    
    def add_resume_coupling_analysis(self,coupling):
        tab_space = 10
        self.set_x(self.get_x() + tab_space)
        independent_exercised = False
        independent_exercised_and_sut_output_affected = False
        text_to_append = ''
        
        for exercise in self.data['individual_coupling_exercises']:
            
            if exercise['id'] == coupling['id']:
                independent_exercised = True
                
                if exercise['sut_output_affected']: 
                    independent_exercised_and_sut_output_affected = True
                    break
                
        self.couplings_color[coupling['id']] =  (0, 100, 0) if independent_exercised_and_sut_output_affected else (255, 0, 0) if independent_exercised else (240, 150, 60)
        
        if('unused_var' in coupling and (coupling['unused_var'] == True)):
            text_to_append = ' | Unused'
            self.couplings_color[coupling['id']] = (74, 37, 17)
            
        
        self.set_font("Arial", "B", 12)
        color = self.couplings_color.get(coupling['id'])
        self.set_text_color(*color)
        self.cell(32, 10, f"- Coupling ID: {coupling['id']}", 10)
        independent_exercised_string = "Yes" if independent_exercised else "No"
        self.cell(58, 10, f" | Independent Exercised: {independent_exercised_string}", 10)
        independent_exercised_and_sut_output_affected_string = "Yes" if independent_exercised_and_sut_output_affected else "No"
        self.cell(0, 10, f"  | Sut Output Affected: {independent_exercised_and_sut_output_affected_string+text_to_append}", 10, 1)
        self.set_text_color(0,0,0)
                
    def add_coupling_section(self, coupling):
        tab_space = 5  # Define o valor do recuo desejado
    
        self.set_x(self.get_x() + tab_space)
        color = self.couplings_color.get(coupling['id'])
        self.set_text_color(*color)
        self.chapter_title(f"Coupling ID: {coupling['id']}")
        self.set_text_color(0,0,0)
        self.ln(-1)
        
        tab_space = 10
        # Tabela para exibir os detalhes do acoplamento
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(52, 6, "Variable:", 0)
        self.set_font("Arial", "", 12)
        self.cell(0, 6, coupling['var'], 0, 1)

        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(52, 6, "Output Component:", 0)
        self.set_font("Arial", "", 12)
        self.cell(0, 6, coupling['output_component'], 0, 1)

        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(52, 6, "Input Component:", 0)
        self.set_font("Arial", "", 12)
        self.cell(0, 6, coupling['input_component'], 0, 1)
        
        # Tabela para exibir os exercícios de acoplamento individuais
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(52, 5, "Non-Varying Parameters:", 0)
        self.set_font("Arial", "", 12)
        non_varying_params = ', '.join(coupling['non_varying_params']) if coupling.get('non_varying_params', False) else 'None'
        self.cell(0, 5, non_varying_params, 0,1)

        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(52, 6, "SUT Outputs Related:", 0)
        self.set_font("Arial", "", 12)
        self.cell(0, 6, ', '.join(coupling['sut_outputs_related']), 0, 1)
        
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(52, 6, "SUT Outputs Affected:", 0)
        self.set_font("Arial", "", 12)
        self.cell(0, 6, ', '.join(coupling['suts_outputs_affected']), 0, 1)
        
        independent_title = True
        pairs = 0
        for exercise in self.data['individual_coupling_exercises']:
            tab_space=15
            if exercise['id'] == coupling['id']:
                pairs += 1
                if independent_title:
                    self.set_x(self.get_x() + 10)
                    self.chapter_title("Independent Coupling Exercises")
                    self.ln(-5)
                    independent_title = False
                # Pares de execuções individuais acoplamentos
                self.set_x(self.get_x() + tab_space)
                self.set_font("Arial", "B", 12)
                self.cell(100, 10, f"{pairs}. Exercised coupling pairs (Test vector lines):", 0)
                self.set_font("Arial", "", 12)
                self.cell(0, 10, ','.join(str(i) for i in exercise['test_vector_pair_lines']), 0, 1)
                self.ln(-2)
                
                tab_space=20
                # Mostrando se os SUT outputs foram afetados
                self.set_x(self.get_x() + tab_space)
                self.set_font("Arial", "B", 12)
                self.cell(70, 5, "SUT Output Affected:", 0)
                self.set_font("Arial", "", 12)
                affected_status = "Yes" if exercise['sut_output_affected'] else "No"
                self.cell(0, 5, affected_status, 0, 1)
                
                sut_outputs_has_no_impact = [key for (key, value) in exercise['suts_outputs_could_be_affected'].items() if not value]
                if(sut_outputs_has_no_impact):
                    self.set_x(self.get_x() + tab_space)
                    self.set_font("Arial", "B", 12)
                    self.cell(71, 5, "Sut Outputs Detected No Impact:", 0)
                    self.set_font("Arial", "", 12)
                    non_varying_values = ', '.join(sut_outputs_has_no_impact)
                    self.cell(0, 5, non_varying_values, 0, 1)
                    
                test_size = 20
                variable_size = 30
                sut_outputs_could_affected_index = {key: idx for idx, (key, value) in enumerate(exercise['suts_outputs_could_be_affected'].items()) if value}
                output_size = len(sut_outputs_could_affected_index)*50
                heigth = 10
                # Tabela para exibir os exercícios de acoplamento individuais
                if(non_varying_params != 'None'):
                    heigth = 15
                    self.set_x(self.get_x() + tab_space)
                    self.set_font("Arial", "B", 12)
                    self.cell(test_size, heigth, 'Test', 1)
                    self.set_font("Arial", "B", 12)
                    self.cell(variable_size, 5, non_varying_params, 1)
                    self.set_font("Arial", "B", 12)
                    self.cell(output_size, 5, ','.join(exercise['non_varying_params_values']), 1)
                    self.ln(5)
                    self.set_x(self.get_x() + test_size + tab_space)
                else:
                    self.set_x(self.get_x() + tab_space)
                    self.set_font("Arial", "B", 12)
                    self.cell(test_size, heigth, 'Test', 1)
                
                # Tabela para exibir os exercícios de acoplamento individuais
                # Adicionando a tabela de execuções
                self.set_font("Arial", "B", 12)
                self.set_font("Arial", "B", 12)
                self.cell(variable_size, 5, "Variable", 1)
                self.cell(output_size, 5, 'Outputs', 1)
                self.ln()
                
                # Tabela para exibir os exercícios de acoplamento individuais
                # Adicionando a tabela de execuções
                self.set_x(self.get_x() + test_size)
                self.set_x(self.get_x() + tab_space)
                self.set_font("Arial", "B", 12)
                self.set_font("Arial", "B", 12)
                self.cell(variable_size, 5, coupling['var'], 1)
                for sut_output_could_affected in sut_outputs_could_affected_index.keys():
                    self.cell(output_size/len(sut_outputs_could_affected_index.keys()), 5, sut_output_could_affected, 1)
                self.ln()
                
                vector_line_index = 0
                for execution in exercise['values_executions']:
                    self.set_x(self.get_x() + test_size)
                    self.set_font("Arial", "", 12)
                    self.cell(test_size, 5, str(exercise['test_vector_pair_lines'][vector_line_index]), 1)
                    self.cell(variable_size, 5, str(execution['var_value']), 1)
                    for idx in sut_outputs_could_affected_index.values():
                        is_the_same = True
                        self.set_text_color(0, 0, 0)
                        if exercise['values_executions'][0]['sut_values'][idx] != exercise['values_executions'][1]['sut_values'][idx]: 
                            is_the_same = False
                            if(not is_the_same): self.set_text_color(0, 128, 0)
                        self.cell(output_size/len(sut_outputs_could_affected_index.keys()), 5, execution['sut_values'][idx], 1)
                        self.set_text_color(0, 0, 0)
                    self.ln()
                    vector_line_index += 1

                self.ln(5)  # Espaço entre seções

def create_report(data, pdf_file_path):
    pdf = PDF(data)  # Passa os dados de log para a instância da classe PDF
    pdf.add_page()
    
    pdf.add_test_results()
    pdf.add_div()    
    
    pdf.add_dc_cc_coverage_section()
    pdf.add_div()
        
    pdf.chapter_title('Detailed Coupling Description')
    for coupling in data['couplings'].values():
        pdf.add_coupling_section(coupling)

    pdf.output(pdf_file_path)
    print(f"PDF report created: {pdf_file_path}")