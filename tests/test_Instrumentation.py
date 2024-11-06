import pytest
from src.Ferramenta_TCC import executar_ferramenta

class TestFI_1:
    # The required inputs are accepted. Using GCC compiler
    def test_1(self, sut_1, sut_1_tv_1):
        test_vector_path = sut_1_tv_1
        sut_path, sut_function_name = sut_1
        compiler_name = 'gcc'
        executar_ferramenta(excel_file_path=test_vector_path, 
                            code_path=sut_path, 
                            function_name=sut_function_name, 
                            compiler=compiler_name)

