from pycparser import c_ast

class FunctionIOAnalyzer(c_ast.NodeVisitor):
    def __init__(self, function_name):
        self.function_name = function_name
        self.inputs = []
        self.outputs = []
        self.all_parameters = []  # Nova lista para todos os parâmetros
        self.param_types = {}

    def visit_FuncDef(self, node):
        if node.decl.name == self.function_name:
            # Captura os parâmetros da função na ordem de declaração
            for param in node.decl.type.args.params:
                param_name = param.name
                self.all_parameters.append(param_name)  # Adiciona à lista AllParameters
                # Verifica se o parâmetro é ponteiro
                if isinstance(param.type, c_ast.PtrDecl):
                    self.param_types[param_name] = 'pointer'
                else:
                    self.param_types[param_name] = 'non_pointer'
            
            # Analisa o corpo da função
            self.visit(node.body)
            
            # Adiciona "returnValue" aos outputs se a função retornar um valor
            if node.decl.type.type.type.names[0] != 'void':
                pass

    def visit_ID(self, node):
        # Verifica se a variável é um parâmetro
        if node.name in self.param_types:
            if self.param_types[node.name] == 'non_pointer':
                # Parâmetro não ponteiro usado em expressão -> input
                if node.name not in self.inputs:
                    self.inputs.append(node.name)
            elif self.param_types[node.name] == 'pointer':
                # Parâmetro ponteiro usado em expressão -> input
                if node.name not in self.inputs:
                    self.inputs.append(node.name)

    def visit_UnaryOp(self, node):
        # Detecta uso de ponteiros na forma *param
        if node.op == '*' and isinstance(node.expr, c_ast.ID):
            param_name = node.expr.name
            if param_name in self.param_types and self.param_types[param_name] == 'pointer':
                # Marca como input se usado em expressão (será revisado em 'visit_Assignment' se for output)
                if param_name not in self.inputs:
                    self.inputs.append(param_name)

    def visit_Assignment(self, node):
        # Lado esquerdo da atribuição (inclui ponteiros e variáveis diretas)
        if isinstance(node.lvalue, c_ast.ID) and node.lvalue.name in self.param_types:
            # Parâmetro que recebe valor -> output
            if self.param_types[node.lvalue.name] == 'pointer' and node.lvalue.name not in self.outputs:
                self.outputs.append(node.lvalue.name)
        elif isinstance(node.lvalue, c_ast.UnaryOp) and node.lvalue.op == '*' and isinstance(node.lvalue.expr, c_ast.ID):
            # Parâmetro ponteiro usado como *param -> output
            param_name = node.lvalue.expr.name
            if param_name in self.param_types and self.param_types[param_name] == 'pointer':
                if param_name not in self.outputs:
                    self.outputs.append(param_name)
        
        # Lado direito da atribuição: verificando se ponteiros são usados como input
        self.visit(node.rvalue)

    def visit_If(self, node):
        # Checa o uso de ponteiros em expressões booleanas dentro de estruturas de controle
        self._check_boolean_expr(node.cond)
        # Visita os blocos da estrutura if
        if node.iftrue:
            self.visit(node.iftrue)
        if node.iffalse:
            self.visit(node.iffalse)

    def _check_boolean_expr(self, expr):
        # Verifica se ponteiros são usados em uma expressão booleana
        if isinstance(expr, c_ast.UnaryOp) and expr.op == '*' and isinstance(expr.expr, c_ast.ID):
            param_name = expr.expr.name
            if param_name in self.param_types and self.param_types[param_name] == 'pointer':
                # Apenas marca como input, não como output
                if param_name not in self.inputs:
                    self.inputs.append(param_name)
        elif isinstance(expr, c_ast.BinaryOp):
            # Verifica ponteiros em expressões binárias
            self._check_boolean_expr(expr.left)
            self._check_boolean_expr(expr.right)

    def analyze(self, ast):
        self.visit(ast)

        # Ordena inputs e outputs de acordo com a ordem dos parâmetros
        ordered_inputs = [p for p in self.all_parameters if p in self.inputs]
        ordered_outputs = [p for p in self.all_parameters if p in self.outputs]

        return ordered_inputs, ordered_outputs, self.all_parameters

def get_component_input_outputs(function_name, ast):
    analyzer = FunctionIOAnalyzer(function_name)
    return analyzer.analyze(ast)
