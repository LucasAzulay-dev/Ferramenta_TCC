from pycparser import c_ast, c_generator, parse_file

class FuncCallVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.generator = c_generator.CGenerator()

    def visit_FuncCall(self, node):
        func_name = self.generator.visit(node.name)

        # Lista de novos statements (incluirá os printf e a chamada original)
        new_statements = []

        # Gerar os argumentos e os printf
        args_before = []
        args_after = []
        args_list_before = []
        args_list_after = []

        for arg in node.args.exprs:
            arg_code = self.generator.visit(arg)
            if isinstance(arg, c_ast.ID):  # Variável normal (não ponteiro)
                print(arg)
                args_before.append(f"{arg_code} = %d")
                args_list_before.append(arg_code)
            elif isinstance(arg, c_ast.UnaryOp) and arg.op == '&':  # Argumento ponteiro
                print(arg)
                pointed_var = self.generator.visit(arg.expr)
                args_after.append(f"{pointed_var} = %d")
                args_list_after.append(f"{pointed_var}")

        # Adicionar printf antes da função
        if args_before:
            printf_before_code = f'"Antes de {func_name}: ' + ', '.join(args_before) + '\\n", ' + ', '.join(args_list_before)
            printf_before = c_ast.FuncCall(c_ast.ID("printf"), c_ast.ExprList([c_ast.Constant(type="string", value=printf_before_code)]))
            new_statements.append(printf_before)

        # A chamada da função original
        new_statements.append(node)

        # Adicionar printf depois da função
        if args_after:
            printf_after_code = f'"Depois de {func_name}: ' + ', '.join(args_after) + '\\n", ' + ', '.join(args_list_after)
            printf_after = c_ast.FuncCall(c_ast.ID("printf"), c_ast.ExprList([c_ast.Constant(type="string", value=printf_after_code)]))
            new_statements.append(printf_after)

        # Retorna os novos statements no lugar da chamada original
        return new_statements

    def generic_visit(self, node):
        if isinstance(node, c_ast.Compound):
            new_block_items = []
            for stmt in (node.block_items or []):
                if isinstance(stmt, c_ast.FuncCall):
                    # Substitui a chamada de função pela versão instrumentada
                    instrumented_statements = self.visit_FuncCall(stmt)
                    new_block_items.extend(instrumented_statements)
            node.block_items = new_block_items
        super().generic_visit(node)

def Create_Intrumented_Code(code_path):
    # Parse o arquivo C
    ast = parse_file(code_path, use_cpp=True, cpp_path='gcc', cpp_args=['-E'])

    # Crie o injetor e aplique ao AST
    injector = FuncCallVisitor()
    injector.visit(ast)

    # Gere o código C com a injeção
    generator = c_generator.CGenerator()
    instrumented_code = generator.visit(ast)
    
    header = '#include <stdio.h>\n'
    instrumented_code_with_header = header + instrumented_code

    # Escreva o código instrumentado em um novo arquivo
    with open('instrumented_SUT.c', 'w') as f:
        f.write(instrumented_code_with_header)

if __name__ == '__main__':
    # Defina o nome do arquivo .c do SUT
    code_path = "SUT.c"
    Create_Intrumented_Code(code_path)
