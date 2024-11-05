from src.Parser import *

class TestMockupProject:
    def filepath(self):
        return '..\\ProjetoMockup\\src\\IntegrationFunction\\IntegrationFunction.c'

    def test_getFuncCalls(self):
        funcDeclList = get_FuncDecls(self.filepath())
        for Decl in funcDeclList:
            Decl.show()
        