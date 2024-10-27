from pycparser import c_ast, parse_file
import re

# Interface ----------------------------------------------------
class cNode:
    def __init__(self, type, name, filename, coordinate):
        self.type = type
        self.name = name
        self.filename = filename
        self.coordinate = coordinate

    def show(self):
        print('('+
              self.type+','+
              self.name+','+
              self.filename+','+
              self.coordinate+
            ')')
        
# TODO: 
# Incluir argumentos das funções
# Get variáveis - declaração, definições, usos
# Incluir variável de retorno nas FunctionCalls
class FunctionArgument:
    def __init__(self, argType, argName, isReference):
        self.argType = argType
        self.argName = argName
        self.isReference = isReference

class FuncCall(cNode):
    def __init__(self, name, filename, coordinate):
        cNode.__init__(self, 'FuncCall', name, filename, coordinate)

class FuncDef(cNode):
    def __init__(self, name, filename, coordinate):
        cNode.__init__(self, 'FuncDef', name, filename, coordinate)

class FuncDecl(cNode):
    def __init__(self, name, filename, coordinate):
        cNode.__init__(self, 'FuncDecl', name, filename, coordinate)

# Node Visitors ------------------------------------------------
class FuncCallVisitor(c_ast.NodeVisitor):
    def __init__(self, funcName):
        self.VisitedList = []
        self.funcName = funcName

    def visit_FuncCall(self, node):
        name = node.name.name
        if self.funcName == '' or self.funcName == name:
            filename, coordinate = _splitCoord(node.name.coord)
            visited = FuncCall(name, filename, coordinate)
            self.VisitedList.append(visited)
        # Visit args in case they contain more func calls.
        if node.args:
            self.visit(node.args)

class FuncDefVisitor(c_ast.NodeVisitor):
    def __init__(self, funcName):
        self.VisitedList = []
        self.funcName = funcName

    def visit_FuncDef(self, node):
        name = node.decl.name
        if self.funcName == '' or self.funcName == name:
            filename, coordinate = _splitCoord(node.decl.coord)
            visited = FuncDef(name, filename, coordinate)
            self.VisitedList.append(visited)

class FuncDeclVisitor(c_ast.NodeVisitor):
    def __init__(self, funcName):
        self.VisitedList = []
        self.funcName = funcName

    def visit_FuncDecl(self, node):
        name = node.type.declname
        if self.funcName == '' or self.funcName == name:
        #     filename, coordinate = _splitCoord(node.name.coord)
            # visited = FuncDecl(name, filename, coordinate)
            visited = FuncDecl(name, '', '')
            self.VisitedList.append(visited)

# Private ------------------------------------------------------------------

def _splitCoord(nodeCoord):
    coordSplit = re.split(':|\\\\', str(nodeCoord))
    filename = coordSplit[-3]
    coordinate = coordSplit[-2]+':'+coordSplit[-1]
    return filename, coordinate

# Public -------------------------------------------------------------------

def get_FuncCalls(filename, funcName=''):
    ast = parse_file(filename, use_cpp=True)
    v = FuncCallVisitor(funcName)
    v.visit(ast)
    return v.VisitedList

def get_FuncDefs(filename, funcName=''):
    ast = parse_file(filename, use_cpp=True)
    v = FuncDefVisitor(funcName)
    v.visit(ast)
    return v.VisitedList

def get_FuncDecls(filename, funcName=''):
    ast = parse_file(filename, use_cpp=True)
    v = FuncDeclVisitor(funcName)
    v.visit(ast)
    return v.VisitedList

if __name__=='__main__':
    filePath = '..\\ProjetoMockup\\src\\IntegrationFunction\\IntegrationFunction.c'
    ast = parse_file(filePath, use_cpp=True)
    