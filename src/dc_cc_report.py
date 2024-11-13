from fpdf import FPDF

class PDF(FPDF):
    def __init__(self, data):
        super().__init__()  # Chama o construtor da classe pai
        self.data = data  # Armazena os dados de log

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
    
    def add_dc_cc_coverage_section(self):
        # Adiciona seção de cobertura com cores baseadas no valor
        self.chapter_title("DC/CC Coverage Summary")
        coverage_percentage = self.data['dc_cc_coverage'] * 100
        color = (0, 128, 0) if coverage_percentage > 85 else (255, 165, 0) if coverage_percentage > 50 else (255, 69, 0)
        self.set_text_color(*color)
        
        tab_space = 5  # Define o valor do recuo desejado
        # Exibe a porcentagem de cobertura
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(0, 5, f"DC/CC Coverage: {coverage_percentage:.1f}%", 30, 30)
        self.set_text_color(0, 0, 0)
        self.ln(5)
        
        # Exibe total de acoplamentos identificados
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(0, 5, f"Identified Couplings: {len(self.data['couplings'])}", 0, 1)
        self.set_text_color(0, 0, 0)
        self.ln(5)
        
        # Exibe total de acoplamento exercitados individualmente que afetaram o sut output
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(0, 5, f"Couplings Exercised Independent and Affecting Outputs: {self.data['couplings_individually_exercised_affected_sut']}", 0, 1)
        self.set_text_color(0, 0, 0)
        self.ln(5)
        
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
        
        for exercise in self.data['individual_coupling_exercises']:
            
            if exercise['id'] == coupling['id']:
                independent_exercised = True
                
                if exercise['sut_outputs_affected']: 
                    independent_exercised_and_sut_output_affected = True
                    break
        
        self.set_font("Arial", "B", 12)
        color = (0, 100, 0) if independent_exercised_and_sut_output_affected else (255, 0, 0) if independent_exercised else (240, 150, 60)
        self.set_text_color(*color)
        self.cell(32, 10, f"- Coupling ID: {coupling['id']}", 10)
        independent_exercised_string = "Yes" if independent_exercised else "No"
        self.cell(58, 10, f" | Independent Exercised: {independent_exercised_string}", 10)
        independent_exercised_and_sut_output_affected_string = "Yes" if independent_exercised_and_sut_output_affected else "No"
        self.cell(0, 10, f"  | Sut Outputs Affected: {independent_exercised_and_sut_output_affected_string}", 10, 1)
        self.set_text_color(0,0,0)
                
    def add_coupling_section(self, coupling):
        tab_space = 5  # Define o valor do recuo desejado
    
        self.set_x(self.get_x() + tab_space)
        self.chapter_title(f"Coupling ID: {coupling['id']}")
        self.ln(-1)
        
        tab_space = 10
        # Tabela para exibir os detalhes do acoplamento
        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(45, 5, "Variable:", 0)
        self.set_font("Arial", "", 12)
        self.cell(0, 5, coupling['var'], 0, 1)

        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(45, 5, "Output Component:", 0)
        self.set_font("Arial", "", 12)
        self.cell(0, 5, coupling['output_component'], 0, 1)

        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(45, 5, "Input Component:", 0)
        self.set_font("Arial", "", 12)
        self.cell(0, 5, coupling['input_component'], 0, 1)

        self.set_x(self.get_x() + tab_space)
        self.set_font("Arial", "B", 12)
        self.cell(45, 5, "SUT Output Related:", 0)
        self.set_font("Arial", "", 12)
        self.cell(0, 5, ', '.join(coupling['sut_outputs_related']), 0, 1)
        
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
                self.cell(100, 5, "SUT Outputs Affected:", 0)
                self.set_font("Arial", "", 12)
                affected_status = "Yes" if exercise['sut_outputs_affected'] else "No"
                self.cell(0, 5, affected_status, 0, 1)
                
                # Tabela para exibir os exercícios de acoplamento individuais
                self.set_x(self.get_x() + tab_space)
                self.set_font("Arial", "B", 12)
                self.cell(100, 5, "Non-Varying Parameters:", 0)
                self.set_font("Arial", "", 12)
                non_varying_params = ', '.join(exercise['non_varying_params']) if exercise['non_varying_params'] else 'None'
                self.cell(0, 5, non_varying_params, 0, 1)

                self.set_x(self.get_x() + tab_space)
                self.set_font("Arial", "B", 12)
                self.cell(100, 5, "Non-Varying Parameters Values:", 0)
                self.set_font("Arial", "", 12)
                non_varying_values = ', '.join(exercise['non_varying_params_values']) if exercise['non_varying_params_values'] else 'None'
                self.cell(0, 5, non_varying_values, 0, 1)

                # Adicionando a tabela de execuções
                self.set_x(self.get_x() + tab_space)
                self.set_font("Arial", "B", 12)
                self.cell(40, 5, coupling['var'], 1)
                self.cell(0, 5, ', '.join(exercise['sut_outputs_related']), 1)
                self.ln()

                for execution in exercise['values_executions']:
                    self.set_x(self.get_x() + tab_space)
                    self.set_font("Arial", "", 12)
                    self.cell(40, 5, str(execution['var_value']), 1)
                    sut_values = ', '.join(map(str, execution['sut_values']))
                    self.cell(0, 5, sut_values, 1)
                    self.ln()

                self.ln(5)  # Espaço entre seções

def create_report(data, pdf_file_path):
    pdf = PDF(data)  # Passa os dados de log para a instância da classe PDF
    pdf.add_page()
    
    pdf.add_dc_cc_coverage_section()
    pdf.add_div()
        
    pdf.chapter_title('Detailed Coupling Description')
    for coupling in data['couplings'].values():
        pdf.add_coupling_section(coupling)

    pdf.output(pdf_file_path)
    print(f"PDF report created: {pdf_file_path}")