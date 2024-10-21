from pycparser import c_parser, c_ast, parse_file

class FuncDefVisitor(c_ast.NodeVisitor):
    def __init__(self, func_name):
        self.func_name = func_name
        self.func_found = False
        self.num_entradas = 0
        self.num_saidas = 0
        self.resultado = []  # Lista que irá armazenar os resultados
    
    def visit_FuncDef(self, node):
        # Verifica se o nome da função corresponde ao procurado
        if node.decl.name == self.func_name:
            self.func_found = True
            
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


def ParseInputOutputs(code_path, target_function):

    # Parsing do código C
    #parser = c_parser.CParser()

    ast = parse_file(code_path, use_cpp=True, cpp_path='gcc', cpp_args=['-E'])
    #ast = parser.parse(code_path)

    # Visitando a árvore de sintaxe
    visitor = FuncDefVisitor(target_function)
    visitor.visit(ast)

    # Exibir a lista de resultados
    return visitor.resultado

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

def gerar_arquivo_h_com_pycparser(arquivo_c):
    # Usar o pycparser para analisar o arquivo .c
    ast = parse_file(arquivo_c, use_cpp=True)
    
    # Visitar nós de definição de função
    visitor = FuncDefVisitor2()
    visitor.visit(ast)
    
    header_path = f'instrumented_SUT.h'

    # Gerar o arquivo .h com as declarações de função
    with open(header_path, 'w') as f:
        f.write('#ifndef _GENERATED_H_\n')
        f.write('#define _GENERATED_H_\n\n')
        for decl in visitor.func_decls:
            f.write(decl + '\n')
        f.write('\n#endif // _GENERATED_H_\n')

if __name__ == '__main__':

    # Defina o nome do arquivo .c do SUT
    code_path = "SUT.c"
    # Função alvo
    target_function = "SUT"

    #resultado = ParseInputOutputs(code_path, target_function)

    gerar_arquivo_h_com_pycparser(code_path)


