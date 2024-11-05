from src.Ferramenta_TCC import executar_ferramenta

# FI#1: A ferramenta deve receber como entrada um SUT, o nome da função a ser testada, 
# um conjunto de testes e o nome de um compilador.
class TestFI_1:
    def SUT(self):
        return '..\\examples\\C_proj_mockup\\SUT\\SUT.c'
    
    def TestVector(self):
        return '..\\examples\\C_proj_mockup\\testvec3.xlsx'

    # The required inputs are accepted. Using GCC compiler
    def test_1(self):
        pathTestVector = self.TestVector()
        pathSUT = self.SUT()
        nameFunctionSUT = 'SUT'
        compilerName = 'gcc'
        executar_ferramenta(pathTestVector, pathSUT, nameFunctionSUT, compilerName)

        