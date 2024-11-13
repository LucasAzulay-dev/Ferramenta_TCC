from pycparser import c_ast, c_generator, parse_file
from Parser import gerar_arquivo_h_com_pycparser
from utils import adicionar_ao_log
from funcoes_extras import list_c_directories

c_type_to_printf = {
    'int': '%d',
    'unsigned int': '%u',
    'short': '%hd',
    'unsigned short': '%hu',
    'long': '%ld',
    'unsigned long': '%lu',
    'float': '%f',
    'double': '%lf',
    'char': '%c',
    'unsigned char': '%c',
    'void': '%p',   # para ponteiros
    'char*': '%s',  # strings
}

class FuncCallVisitor(c_ast.NodeVisitor):
    def __init__(self, func_name):
        self.func_name = func_name
        self.generator = c_generator.CGenerator()
        self.instrument_sut = False  # Para controlar se estamos dentro de SUT
        self.execution_order = 1
        self.variables = {}  # Armazenamento de variáveis e tipos
        self.output_variables = []

    def visit_FuncDef(self, node):
		# Verificar se estamos na definição da função SUT
        if node.decl.name == self.func_name:
            self.instrument_sut = True
            self.generic_visit(node)
            print(self.variables)
            self.instrument_sut = False
        else:
            pass

    def visit_FuncCall(self, node):
        if self.instrument_sut:
            func_name = self.generator.visit(node.name)
            new_statements = []
            args_in = {}
            args_out = {}
            args_sut_out = {}

            # Coletar argumentos de entrada
            for arg in node.args.exprs:
                var = self.generator.visit(arg)
                if isinstance(arg, c_ast.ID) and (var not in self.output_variables):  # Variável normal
                    args_in[var] = c_type_to_printf.get(self.variables.get(var))
                elif isinstance(arg, c_ast.UnaryOp) and arg.op == '&' and (var not in self.output_variables):  # Ponteiro
                    pointed_var = self.generator.visit(arg.expr)
                    args_out[pointed_var] = c_type_to_printf.get(self.variables.get(pointed_var)) # SUT Output
                elif (var in self.output_variables):
                    args_sut_out[var] = c_type_to_printf.get(self.variables.get(var))
                    

            # Chamada da função original
            new_statements.append(node)

            # Adicionar sprintf para registrar dados em JSON após a função
            execution_order_str = f'{self.execution_order}'
            self.execution_order += 1

            args_in_json = [f'\\"{key}\\": \\"{value}\\"' for key, value in args_in.items()]
            args_out_json = [f'\\"{key}\\": \\"{value}\\"' for key, value in args_out.items()]
            args_sut_out_json = [f'\\"{key}\\": \\"{value}\\"' for key, value in args_sut_out.items()]

            json_entry = '\"' + (
            f'{{\\"function\\": \\"{func_name}\\", '
            f'\\"executionOrder\\": \\"{execution_order_str}\\", '
            f'\\"in\\": {{{",".join(args_in_json)}}}, '
            f'\\"out\\": {{{",".join(args_out_json)+",".join(args_sut_out_json)}}}}}'
            ) + ',\\n\"'
            
            args = ','.join([f'{key}' for key in args_in.keys()] + [f'{key}' for key in args_out.keys()] + [f'*{key}' for key in args_sut_out.keys()])

            # Adicionar o sprintf direto para registrar no log_buffer acumulativamente
            new_statements.append(c_ast.FuncCall(
                c_ast.ID("sprintf"),
                c_ast.ExprList([
                    c_ast.BinaryOp('+', c_ast.ID("log_buffer"), c_ast.FuncCall(c_ast.ID("strlen"), c_ast.ExprList([c_ast.ID("log_buffer")]))),
                    c_ast.Constant(type="string", value=json_entry + ','+ args)
                ])
            ))

            return new_statements
        else:
            return node
    
    def visit_Assignment(self, node):
        if self.instrument_sut and isinstance(node.rvalue, c_ast.FuncCall):
            func_call = node.rvalue
            func_name = self.generator.visit(func_call.name)

            new_statements = []
            args_in = {}
            args_out = {}
            args_sut_out = {}

            # Coletar argumentos de entrada e saída para a função chamada
            for arg in func_call.args.exprs:
                var = self.generator.visit(arg)
                if isinstance(arg, c_ast.ID) and (var not in self.output_variables):
                    args_in[var] = c_type_to_printf.get(self.variables.get(var))
                elif isinstance(arg, c_ast.UnaryOp) and arg.op == '&' and (var not in self.output_variables):
                    pointed_var = self.generator.visit(arg.expr)
                    args_out[pointed_var] = c_type_to_printf.get(self.variables.get(pointed_var))
                elif (var in self.output_variables):
                    args_sut_out[var] = c_type_to_printf.get(self.variables.get(var))

            # Verificar se a variável à esquerda da atribuição deve ser uma saída
            if isinstance(node.lvalue, c_ast.ID):
                var = self.generator.visit(node.lvalue)
                args_out[var] = c_type_to_printf.get(self.variables.get(var))
            elif isinstance(node.lvalue, c_ast.UnaryOp) and node.lvalue.op == '*':
                # Se for um ponteiro (como *b), marcamos como uma saída da função chamada
                pointed_var = self.generator.visit(node.lvalue.expr)
                args_out[pointed_var] = c_type_to_printf.get(self.variables.get(pointed_var))
                # Também marcamos como uma saída geral da função SUT
                self.output_variables.append(pointed_var)

            # Chamada original da função
            new_statements.append(node)

            # Log em JSON após a chamada da função
            execution_order_str = f'{self.execution_order}'
            self.execution_order += 1

            args_in_json = [f'\\"{key}\\": \\"{value}\\"' for key, value in args_in.items()]
            args_out_json = [f'\\"{key}\\": \\"{value}\\"' for key, value in args_out.items()]
            args_sut_out_json = [f'\\"{key}\\": \\"{value}\\"' for key, value in args_sut_out.items()]

            json_entry = '\"' + (
                f'{{\\"function\\": \\"{func_name}\\", '
                f'\\"executionOrder\\": \\"{execution_order_str}\\", '
                f'\\"in\\": {{{",".join(args_in_json)}}}, '
                f'\\"out\\": {{{",".join(args_out_json + args_sut_out_json)}}}}}'
            ) + ',\\n\"'

            args = ','.join([f'{key}' for key in args_in.keys()] + [f'{key}' for key in args_out.keys()] + [f'*{key}' for key in args_sut_out.keys()])

            # Registro no log_buffer
            new_statements.append(c_ast.FuncCall(
                c_ast.ID("sprintf"),
                c_ast.ExprList([
                    c_ast.BinaryOp('+', c_ast.ID("log_buffer"), c_ast.FuncCall(c_ast.ID("strlen"), c_ast.ExprList([c_ast.ID("log_buffer")]))),
                    c_ast.Constant(type="string", value=json_entry + ',' + args)
                ])
            ))

            return new_statements

        return node

    def generic_visit(self, node):
        new_block_items = []

        if isinstance(node, c_ast.TypeDecl):
            var_name = node.declname
            var_type = ''.join(node.type.names)
            self.variables[var_name] = var_type
            
        if self.instrument_sut and isinstance(node, c_ast.FuncDecl):
            for params in node.args.params:
                if isinstance(params.type, c_ast.PtrDecl):
                    self.output_variables.append(params.name)
        
        if self.instrument_sut and isinstance(node, c_ast.Compound):
            for stmt in (node.block_items or []):
                if isinstance(stmt, c_ast.FuncCall):
                    instrumented_statements = self.visit_FuncCall(stmt)
                    new_block_items.extend(instrumented_statements)
                elif isinstance(stmt, c_ast.Assignment):
                    instrumented_statements = self.visit_Assignment(stmt)
                    new_block_items.extend(instrumented_statements)
                else:
                     new_block_items.append(stmt)
            node.block_items = new_block_items
           
        super().generic_visit(node)

    def visit_Return(self, node):
        if self.instrument_sut:
            new_statements = []
            args_out = {}

            # Registrar a saída de retorno e garantir que tenha o tipo correto para impressão
            if isinstance(node.expr, c_ast.ID):
                var = self.generator.visit(node.expr)
                var_type = self.variables.get(var)
                # Usar o tipo encontrado ou um fallback se o tipo não for encontrado
                args_out[var] = c_type_to_printf.get(var_type)  

            # Registrar todas as variáveis na lista de saída
            for var in self.output_variables:
                if var not in args_out:
                    var_type = self.variables.get(var)
                    args_out[var] = c_type_to_printf.get(var_type)  

            execution_order_str = f'{self.execution_order}'
            self.execution_order += 1

            args_out_json = [f'\\"{key}\\": \\"{value}\\"' for key, value in args_out.items()]

            json_entry = '\"' + (
                f'{{\\"function\\": \\"{self.func_name}\\", '
                f'\\"executionOrder\\": \\"{execution_order_str}\\", '
                f'\\"out\\": {{{",".join(args_out_json)}}}}}'
            ) + ',\\n\"'

            args = ','.join([f'{key}' for key in args_out.keys()])

            # Adicionar sprintf para registrar o retorno no log_buffer
            new_statements.append(c_ast.FuncCall(
                c_ast.ID("sprintf"),
                c_ast.ExprList([
                    c_ast.BinaryOp('+', c_ast.ID("log_buffer"), c_ast.FuncCall(c_ast.ID("strlen"), c_ast.ExprList([c_ast.ID("log_buffer")]))),
                    c_ast.Constant(type="string", value=json_entry + ',' + args)
                ])
            ))

            # Adiciona o retorno real no final
            new_statements.append(node)

            return new_statements
        else:
            return node


def Create_Instrumented_Code(folder_path, SUT_path, function_name, bufferLength):
    try:
        adicionar_ao_log("Starting code instrumentation...")
        # Parse o arquivo C
        compile_headers_path = list_c_directories(folder_path, SUT_path)
        cpp_args = ['-E'] + compile_headers_path
        ast = parse_file(SUT_path, use_cpp=True, cpp_path='gcc', cpp_args= cpp_args)

        # Crie o injetor e aplique ao AST
        injector = FuncCallVisitor(function_name)
        injector.visit(ast)

        # Gere o código C com a injeção
        generator = c_generator.CGenerator()
        instrumented_code = generator.visit(ast)
        
        # Adiciona cabeçalho para log_buffer e sprintf
        header = f'#include <stdio.h>\n#include <string.h>\n#include "instrumented_SUT.h"\nextern char log_buffer[{bufferLength}];\n'
        instrumented_code_with_header = header + instrumented_code

        # Escreva o código instrumentado em um novo arquivo
        with open(r'output\InstrumentedSUT\instrumented_SUT.c', 'w') as f:
            f.write(instrumented_code_with_header)

        gerar_arquivo_h_com_pycparser(SUT_path, cpp_args)

        adicionar_ao_log("Instrumentation completed.")
        return 0
    except:
        error = f"ERROR: Instrumentation not executed properly." # {e.stderr}
        adicionar_ao_log(error)
        return error
    
if __name__ == '__main__':

    # Defina o nome do arquivo .c do SUT
    SUT_path = "tests\\test_cases\\functional_cases\\case2\\src\\SUT\\SUT.c" 

    # Defina o nome do arquivo .c do SUT
    folder_path = "tests\\test_cases\\functional_cases\\case2\\src" 

    # Defina o nome da função testada
    function_name = "SUT"

    bufferLength = 4096

    Create_Instrumented_Code(folder_path, SUT_path, function_name, bufferLength)
    