from pycparser import c_parser, c_ast, parse_file
from utils import adicionar_ao_log
from funcoes_extras import list_c_directories

class FuncDefVisitor(c_ast.NodeVisitor):
    def __init__(self, func_name):
        self.func_name = func_name
        self.func_found = False
        self.num_entradas = 0
        self.num_saidas = 0
        self.resultado = []  # Lista que irá armazenar os resultados
        self.error_message = ''
   
    def visit_FuncDef(self, node):
        # Verifica se o nome da função corresponde ao procurado
        if node.decl.name == self.func_name:
            self.func_found = True

            # Verifica se a função possui parâmetros
            if node.decl.type.args is None or len(node.decl.type.args.params) == 0:
                self.error_message = f"ERROR: function '{self.func_name}' has no parameters."
                return
           
            # Obtendo os parâmetros da função
            params = node.decl.type.args.params
            for param in params:
                param_type = self._get_type(param.type)
                param_kind = "O" if self._is_pointer(param.type) else "I"
               
                # Contagem de entradas e saídas
                if param_kind == "I":
                    self.num_entradas += 1
                else:
                    self.num_saidas += 1


                # Adicionando à lista separadamente o tipo do parâmetro e se é Entrada (I) ou Saída (O)
                self.resultado.append(param_kind)  # Primeiro, Entrada (I) ou Saída (O)
                self.resultado.append(param_type)  # Depois, o tipo do parâmetro
           
            # Adiciona o número de entradas e saídas ao início da lista
            self.resultado.insert(0, self.num_saidas)  # Segundo item: número de saídas
            self.resultado.insert(0, self.num_entradas)  # Primeiro item: número de entradas
   
    def _get_type(self, type_node):
        """ Função auxiliar para obter o tipo de um nó """
        if isinstance(type_node, c_ast.PtrDecl):
            return self._get_type(type_node.type)   # Ponteiro  + '*'
        elif isinstance(type_node, c_ast.TypeDecl):
            return ' '.join(type_node.type.names)  # Tipos como "unsigned int"
        return "desconhecido"


    def _is_pointer(self, type_node):
        """ Função auxiliar para verificar se um nó é ponteiro """
        return isinstance(type_node, c_ast.PtrDecl)
    
    def check_errors(self):
        """ Função que checa se houve erros e retorna as mensagens correspondentes """
        if not self.func_found:
            return f"ERROR: function '{self.func_name}' not found."
        if self.error_message:
            return self.error_message
        return None

class FuncReturnVisitor(c_ast.NodeVisitor):
    def __init__(self, target_function_name):
        self.target_function_name = target_function_name
        self.var_return_info = []  # Lista para armazenar "OR" e o tipo da variável
        self.in_target_function = False
        self.current_declared_vars = {}

    def visit_FuncDef(self, node):
        # Verifica se a função atual é a função alvo
        if node.decl.name == self.target_function_name:
            self.in_target_function = True
            self.current_declared_vars = {}  # Limpa o dicionário de variáveis declaradas
            # Visita o corpo da função
            self.visit(node.body)
            self.in_target_function = False

    def visit_Decl(self, node):
        # Captura as variáveis declaradas dentro da função alvo
        if self.in_target_function and isinstance(node.type, c_ast.TypeDecl):
            var_type = node.type.type.names[0]  # Tipo da variável (ex: int, float)
            self.current_declared_vars[node.name] = var_type

    def visit_Return(self, node):
        # Verifica se o return está dentro da função alvo e retorna uma variável
        if self.in_target_function and not self.var_return_info:
            if isinstance(node.expr, c_ast.ID):
                var_name = node.expr.name
                var_type = self.current_declared_vars.get(var_name)
                if var_type:
                    # Adiciona "OR" e o tipo como itens separados na lista
                    self.var_return_info.append("OR")
                    self.var_return_info.append(var_type)


def ParseInputOutputs(code_path, folder_path, target_function):

    # Parsing do código C
    compile_headers_path = list_c_directories(folder_path, code_path)
    cpp_args = ['-E'] + compile_headers_path
    ast = parse_file(code_path, use_cpp=True, cpp_path='gcc', cpp_args= cpp_args)


    # Visitando a árvore de sintaxe
    visitor = FuncDefVisitor(target_function)
    visitor.visit(ast)


    visitor_return = FuncReturnVisitor(target_function)
    visitor_return.visit(ast)

    # Checando se houve erros
    error = visitor.check_errors()

    if (error):
        return error

    if(len(visitor_return.var_return_info) > 0):
        visitor.resultado[1] += 1

    lista_resultante = visitor.resultado + visitor_return.var_return_info

    # Exibir a lista de resultados
    return lista_resultante

class FuncDefVisitor2(c_ast.NodeVisitor):
    def __init__(self):
        self.func_decls = []

    def visit_FuncDef(self, node):
        # Extrair tipo de retorno
        tipo_retorno = self._get_type(node.decl.type)

        # Nome da função
        nome_funcao = node.decl.name

        # Extrair parâmetros
        parametros = []
        if isinstance(node.decl.type.args, c_ast.ParamList):
            for param in node.decl.type.args.params:
                param_tipo = self._get_type(param.type)
                param_nome = param.name if param.name else ''
                parametros.append(f'{param_tipo} {param_nome}'.strip())
        else:
            parametros.append('void')

        # Montar a declaração da função
        declaracao = f'{tipo_retorno} {nome_funcao}({", ".join(parametros)});'
        self.func_decls.append(declaracao)

    def _get_type(self, tipo):
        """ Função auxiliar para extrair o tipo correto, incluindo ponteiros e outros tipos compostos """
        if isinstance(tipo, c_ast.TypeDecl):
            if isinstance(tipo.type, c_ast.IdentifierType):
                return ' '.join(tipo.type.names)
        elif isinstance(tipo, c_ast.PtrDecl):  # Para tipos com ponteiros
            return self._get_type(tipo.type) + '*'
        elif isinstance(tipo, c_ast.ArrayDecl):  # Para arrays
            return self._get_type(tipo.type) + '[]'
        elif isinstance(tipo, c_ast.FuncDecl):  # Para funções como ponteiros
            return self._get_type(tipo.type)
        return 'void'

def gerar_arquivo_h_com_pycparser(arquivo_c, cpp_args):
    adicionar_ao_log("Generating .h file with pycparser...")
    # Usar o pycparser para analisar o arquivo .c
    ast = parse_file(arquivo_c, use_cpp=True,cpp_args=cpp_args)
    
    # Visitar nós de definição de função
    visitor = FuncDefVisitor2()
    visitor.visit(ast)
    
    header_path = r'output\InstrumentedSUT\instrumented_SUT.h'

    # Gerar o arquivo .h com as declarações de função
    with open(header_path, 'w') as f:
        f.write('#ifndef _GENERATED_H_\n')
        f.write('#define _GENERATED_H_\n\n')
        for decl in visitor.func_decls:
            f.write(decl + '\n')
        f.write('\n#endif // _GENERATED_H_\n')
    
    adicionar_ao_log(".h file generated successfully.")

#------------------------------------------------------------------------------------------------------

class FuncDefVisitor3(c_ast.NodeVisitor):
    def __init__(self, func_name):
        self.func_name = func_name
        self.inputs = []  # Lista para armazenar nomes de variáveis de entrada
        self.outputs = []  # Lista para armazenar nomes de variáveis de saída (incluindo retornos)
        self.current_declared_vars = {}  # Dicionário para armazenar as declarações de variáveis locais

    def visit_FuncDef(self, node):
        # Verifica se o nó é a função alvo
        if node.decl.name == self.func_name:
            params = node.decl.type.args.params
            # Processa os parâmetros da função
            for param in params:
                param_name = param.name  # Nome da variável
                param_kind = "O" if self._is_pointer(param.type) else "I"
                
                # Adiciona o nome da variável à lista correta
                if param_kind == "I":
                    self.inputs.append(param_name)
                else:
                    self.outputs.append(param_name)
            
            # Visita o corpo da função para capturar retornos
            self.visit(node.body)

    def visit_Decl(self, node):
        # Captura variáveis declaradas dentro da função
        if isinstance(node.type, c_ast.TypeDecl):
            var_type = node.type.type.names[0]
            self.current_declared_vars[node.name] = var_type

    def visit_Return(self, node):
        # Verifica se o retorno é uma variável e adiciona seu nome à lista de saídas
        if isinstance(node.expr, c_ast.ID):
            var_name = node.expr.name
            if var_name not in self.outputs:  # Evita duplicações
                self.outputs.append(var_name)

    def _is_pointer(self, type_node):
        """ Função auxiliar para verificar se um nó é ponteiro """
        return isinstance(type_node, c_ast.PtrDecl)

    def get_results(self):
        """ Retorna as listas de entradas e saídas como strings formatadas """
        formatted_inputs = '[{}]'.format(", ".join(f'"{name}"' for name in self.inputs))
        formatted_outputs = '[{}]'.format(", ".join(f'"{name}"' for name in self.outputs))
        return formatted_inputs, formatted_outputs


def ParseNameInputsOutputs(code_path, folder_path, target_function):

    # Parsing do código C

    compile_headers_path = list_c_directories(folder_path, code_path)
    cpp_args = ['-E'] + compile_headers_path
    ast = parse_file(code_path, use_cpp=True, cpp_path='gcc', cpp_args= cpp_args)

    # Visitando a árvore de sintaxe
    visitor = FuncDefVisitor3(target_function)
    visitor.visit(ast)

    inputs, outputs = visitor.get_results()

    # Exibir a lista de resultados
    return inputs, outputs

#------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # Defina o nome do arquivo .c do SUT
    code_path = "tests/test_cases/case2/src/SUT/SUT2.c"
    # Função alvo
    target_function = "SUT"

    folder_path= "tests/test_cases/case2/src/SUT"

    #resultado = ParseInputOutputs(code_path, target_function)
    #print(resultado)

    #gerar_arquivo_h_com_pycparser(code_path)

    inputs, outputs = ParseNameInputsOutputs(code_path, folder_path ,target_function)

    print("Inputs:", inputs)
    print("Outputs:", outputs)