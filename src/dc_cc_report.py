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
        
        # Exibe a porcentagem de cobertura
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"DC/CC Coverage: {coverage_percentage:.1f}%", 0, 1)
        self.set_text_color(0, 0, 0)
        self.ln(5)

    def add_coupling_section(self, coupling):
        self.chapter_title(f"Coupling ID: {coupling['id']}")

        # Tabela para exibir os detalhes do acoplamento
        self.set_font("Arial", "B", 12)
        self.cell(45, 10, "Variable:", 0)
        self.set_font("Arial", "", 12)
        self.cell(0, 10, coupling['var'], 0, 1)

        self.set_font("Arial", "B", 12)
        self.cell(45, 10, "Output Component:", 0)
        self.set_font("Arial", "", 12)
        self.cell(0, 10, coupling['output_component'], 0, 1)

        self.set_font("Arial", "B", 12)
        self.cell(45, 10, "Input Component:", 0)
        self.set_font("Arial", "", 12)
        self.cell(0, 10, coupling['input_component'], 0, 1)

        self.set_font("Arial", "B", 12)
        self.cell(45, 10, "SUT Output Related:", 0)
        self.set_font("Arial", "", 12)
        self.cell(0, 10, ', '.join(coupling['sut_outputs_related']), 0, 1)
        self.ln(5)  # Espaço entre seções

        individual_coupling_title = 0
        for exercise in self.data['individual_coupling_exercises']:
            if exercise['id'] == coupling['id']:
                if individual_coupling_title == 0:
                    self.chapter_title("Individual Coupling Exercises")
                    individual_coupling_title = 1
                
                # Pares de execuções individuais acoplamentos
                self.set_font("Arial", "B", 12)
                self.cell(100, 10, "Exercised coupling pairs (Test vector lines):", 0)
                self.set_font("Arial", "", 12)
                self.cell(0, 10, ','.join(str(i) for i in exercise['test_vector_pair_lines']), 0, 1)
                self.ln(2)

                # Mostrando se os SUT outputs foram afetados
                self.set_font("Arial", "B", 12)
                self.cell(100, 10, "SUT Outputs Affected:", 0)
                self.set_font("Arial", "", 12)
                affected_status = "Yes" if exercise['sut_outputs_affected'] else "No"
                self.cell(0, 10, affected_status, 0, 1)
                self.ln(2)
                
                # Tabela para exibir os exercícios de acoplamento individuais
                self.set_font("Arial", "B", 12)
                self.cell(100, 10, "Non-Varying Parameters:", 0)
                self.set_font("Arial", "", 12)
                non_varying_params = ', '.join(exercise['non_varying_params']) if exercise['non_varying_params'] else 'None'
                self.cell(0, 10, non_varying_params, 0, 1)

                self.set_font("Arial", "B", 12)
                self.cell(100, 10, "Non-Varying Parameters Values:", 0)
                self.set_font("Arial", "", 12)
                non_varying_values = ', '.join(exercise['non_varying_params_values']) if exercise['non_varying_params_values'] else 'None'
                self.cell(0, 10, non_varying_values, 0, 1)

                # Adicionando a tabela de execuções
                self.set_font("Arial", "B", 12)
                self.cell(40, 10, coupling['var'], 1)
                self.cell(0, 10, ', '.join(exercise['sut_outputs_related']), 1)
                self.ln()

                for execution in exercise['values_executions']:
                    self.set_font("Arial", "", 12)
                    self.cell(40, 10, str(execution['var_value']), 1)
                    sut_values = ', '.join(map(str, execution['sut_values']))
                    self.cell(0, 10, sut_values, 1)
                    self.ln()

                self.ln(5)  # Espaço entre seções

def create_report(data, pdf_file_path):
    pdf = PDF(data)  # Passa os dados de log para a instância da classe PDF
    pdf.add_page()
    
    print
    
    pdf.add_dc_cc_coverage_section()
    
    # pdf.add_section_div()
    
    # pdf.add_resume_coupling_analysis()
    
    # pdf.add_section_div()

    for coupling in data['couplings'].values():
        pdf.add_coupling_section(coupling)

    pdf.output(pdf_file_path)
    print(f"PDF report created: {pdf_file_path}")