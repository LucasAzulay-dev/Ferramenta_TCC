from pycparser import c_ast, parse_file, c_parser,c_generator
from utils import adicionar_ao_log, list_c_directories
import os
import re

class FuncDefVisitor(c_ast.NodeVisitor):
    def __init__(self, func_name):
        self.func_name = func_name
        self.func_found = False
        self.num_param = 0
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
                self.num_param += 1
                self.resultado.append(param_type) 
           
            self.resultado.insert(0, self.num_param)  
   
    def _get_type(self, type_node):
        """ Função auxiliar para obter o tipo de um nó """
        if isinstance(type_node, c_ast.PtrDecl):
            return self._get_type(type_node.type)   # Ponteiro  + '*'
        elif isinstance(type_node, c_ast.TypeDecl):
            return ' '.join(type_node.type.names)  # Tipos como "unsigned int"


    def check_errors(self):
        """ Função que checa se houve erros e retorna as mensagens correspondentes """
        if not self.func_found:
            return f"ERROR: function '{self.func_name}' not found."
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
            # Visita o corpo da função
            self.visit(node.body)
            self.in_target_function = False
            self.current_declared_vars = {}  # Limpa o dicionário de variáveis declaradas

    def visit_Decl(self, node):
        # Captura as variáveis declaradas dentro da função alvo
        if isinstance(node.type, c_ast.TypeDecl):
            var_type = node.type.type.names[0]  # Tipo da variável (ex: int, float)
            self.current_declared_vars[node.name] = var_type

    def visit_Return(self, node):
        # Verifica se o return está dentro da função alvo e retorna uma variável
        if self.in_target_function and not self.var_return_info:
            if isinstance(node.expr, c_ast.ID):
                var_name = node.expr.name
                var_type = self.current_declared_vars.get(var_name)
                if var_type:
                    self.var_return_info.append(var_type)


def ParseInputOutputs(ast, target_function):

    # Visitando a árvore de sintaxe
    visitor = FuncDefVisitor(target_function)
    visitor.visit(ast)


    visitor_return = FuncReturnVisitor(target_function)
    visitor_return.visit(ast)

    # Checando se houve erros
    error = visitor.check_errors()

    if (error):
        raise Exception(error)

    if(len(visitor_return.var_return_info) > 0):
        visitor.resultado[0] += 1
        visitor.resultado.insert(1,"return")
    else:
        visitor.resultado.insert(1,"noreturn")

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
        # else:
        #     parametros.append('void')

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
        # elif isinstance(tipo, c_ast.ArrayDecl):  # Para arrays
        #     return self._get_type(tipo.type) + '[]'
        elif isinstance(tipo, c_ast.FuncDecl):  # Para funções como ponteiros
            return self._get_type(tipo.type)
        return 'void'

def gerar_arquivo_h_com_pycparser(ast):
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
        self.outputs = {}  # Lista para armazenar nomes de variáveis de saída (incluindo retornos)
        self.current_declared_vars = {}  # Dicionário para armazenar as declarações de variáveis locais
        self.variables = {}  # Dicionário para armazenar as declarações de variáveis locais

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
                    self.variables[param_name] = ''.join(param.type.type.names)
                else:
                    self.outputs[param_name] = '*'
                    self.variables[param_name] = ''.join(param.type.type.type.names)
                
            
            # Visita o corpo da função para capturar retornos
            self.visit(node.body)

    def visit_Decl(self, node):
        # Captura variáveis declaradas dentro da função
        if isinstance(node.type, c_ast.TypeDecl):
            var_type = node.type.type.names[0]
            self.current_declared_vars[node.name] = var_type
            self.variables[node.name] = var_type

    def visit_Return(self, node):
        # Verifica se o retorno é uma variável e adiciona seu nome à lista de saídas
        if isinstance(node.expr, c_ast.ID):
            var_name = node.expr.name
            if var_name not in self.outputs:  # Evita duplicações
                self.outputs[var_name] = ''

    def _is_pointer(self, type_node):
        """ Função auxiliar para verificar se um nó é ponteiro """
        return isinstance(type_node, c_ast.PtrDecl)

    def get_results(self):
            """ Retorna as listas de entradas e saídas como strings formatadas """
            formatted_inputs = '[{}]'.format(", ".join(f'\"{name}\"' for name in self.inputs))
            formatted_outputs = '[{}]'.format(", ".join(f'\"{name}\"' for name in self.outputs.keys()))
            return formatted_inputs.replace('"', '\\"'), formatted_outputs.replace('"', '\\"')
        
    def get_variables_and_sut_outputs(self):
            return self.variables, self.outputs


def ParseVariablesAndSutOutputs(ast, target_function):
    # Visitando a árvore de sintaxe
    visitor = FuncDefVisitor3(target_function)
    visitor.visit(ast)

    inputs, outputs = visitor.get_variables_and_sut_outputs()

    # Exibir a lista de resultados
    return inputs, outputs

def ParseNameInputsOutputs(ast, target_function):
    # Visitando a árvore de sintaxe
    visitor = FuncDefVisitor3(target_function)
    visitor.visit(ast)

    inputs, outputs = visitor.get_results()

    # Exibir a lista de resultados
    return inputs, outputs

#------------------------------------------------------------------------------------------------------
def substitute_headers_with_sources(main_file):
    combined_code = []

    # Lê o arquivo principal
    with open(main_file, 'r') as f:
        main_file_normalized = os.path.normpath(main_file)
        for line in f:
            if line.strip().startswith('#include') or line.strip().startswith('# include'):
                # Verifica se é um include de um header relativo
                try:
                    header_path = line.strip().split('"')[1]
                    header_path = os.path.normpath(os.path.join(os.path.dirname(main_file), header_path))

                    # Substitui o header pelo conteúdo correspondente do .c, se disponível
                    source_path = header_path.replace('.h', '.c')
                    if(source_path != main_file_normalized):
                        if os.path.exists(source_path):
                            with open(source_path, 'r') as source_file:
                                for line_source_file in source_file:
                                    if not line_source_file.strip().startswith('#'):
                                        combined_code.append(line_source_file)
                        elif line.strip().startswith('#') :
                            pass
                        else:
                            combined_code.append(line)  # Mantém o include se não encontrar o .c
                except:
                    pass
            else:
                combined_code.append(line)

    return clean_c_code(''.join(combined_code)) # Retorna o código combinado como uma string

def clean_c_code(code):
    # 1. Remover comentários de linha (//)
    code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)

    # 2. Remover comentários de bloco (/* ... */)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

    # 3. Remover diretivas de pré-processador como #include, #define, #ifdef, etc.
    code = re.sub(r'^\s*#.*$', '', code, flags=re.MULTILINE)

    # 4. Opcional: Remover linhas em branco
    code = re.sub(r'^\s*$', '', code, flags=re.MULTILINE)

    return code

def generate_ast(code_path):
    code = (substitute_headers_with_sources(code_path))
    parser = c_parser.CParser()
    return parser.parse(code)