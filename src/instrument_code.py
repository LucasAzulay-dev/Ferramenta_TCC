from pycparser import c_ast, c_generator, parse_file
from Parser import gerar_arquivo_h_com_pycparser
from utils import adicionar_ao_log
from Parser import ParseVariablesAndSutOutputs, generate_ast
from getInputOutputs import get_component_input_outputs
import copy

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
        self.output_variables = {}
        self.components_inputs = {}
        self.components_outputs = {}
        
    def build_sut_variables_and_outputs(self, ast, target_function):
        nameInputsOutputs = ParseVariablesAndSutOutputs(ast, target_function)
        self.variables = nameInputsOutputs[0]
        self.output_variables = {key: '*' for key in nameInputsOutputs[1]}
        
    def visit_FuncDef(self, node):
		# Verificar se estamos na definição da função SUT
        function_name = node.decl.name
        if function_name == self.func_name:
            self.instrument_sut = True
            self.generic_visit(node)
            #print(self.variables)
            self.instrument_sut = False
        else:
            inputs, outputs = get_component_input_outputs(function_name, node)
            self.components_inputs[function_name] = inputs
            self.components_outputs[function_name] = outputs

    def visit_FuncCall(self, node):
        if self.instrument_sut:
            func_name = self.generator.visit(node.name)
            if(func_name != 'sprintf'):
                new_statements = []

                # Adicionar sprintf para registrar dados em JSON após a função
                execution_order_str = f'{self.execution_order}'
                self.execution_order += 1

                args_in_json = [f'\\"{key}\\": \\"{c_type_to_printf.get(self.variables.get(key))}\\"' for key in self.components_inputs.get(func_name)]
                json_entry_before_call = r'"'+(
                f'{{\\"function\\": \\"{func_name}\\", '
                f'\\"executionOrder\\": \\"{execution_order_str}\\", '
                f'\\"in\\": {{{",".join(args_in_json)}}}'
                ) + r',"'
                args_before_call = ','.join([f'{key}' for key in self.components_inputs.get(func_name)])
                
                new_statements.append(c_ast.FuncCall(
                    c_ast.ID("sprintf"),
                    c_ast.ExprList([
                        c_ast.BinaryOp('+', c_ast.ID("log_buffer"), c_ast.FuncCall(c_ast.ID("strlen"), c_ast.ExprList([c_ast.ID("log_buffer")]))),
                        c_ast.Constant(type="string", value=json_entry_before_call + ','+ args_before_call)
                    ])
                ))

                # Chamada da função original
                new_statements.append(node)
                
                args_out_json = [f'\\"{key}\\": \\"{c_type_to_printf.get(self.variables.get(key))}\\"' for key in self.components_outputs.get(func_name)]
                json_entry_after_call = r'"'+(
                f'\\"out\\": {{{",".join(args_out_json)}}}'
                ) + r'},", '
                args_after_call = ','.join(
                [f'*{key}' if key in self.output_variables else key for key in self.components_outputs.get(func_name)]
                )
                
                # Adicionar o sprintf direto para registrar no log_buffer acumulativamente
                new_statements.append(c_ast.FuncCall(
                    c_ast.ID("sprintf"),
                    c_ast.ExprList([
                        c_ast.BinaryOp('+', c_ast.ID("log_buffer"), c_ast.FuncCall(c_ast.ID("strlen"), c_ast.ExprList([c_ast.ID("log_buffer")]))),
                        c_ast.Constant(type="string", value=json_entry_after_call + args_after_call)
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

            if isinstance(node.lvalue, c_ast.PtrDecl) or isinstance(node.lvalue, c_ast.ID) or isinstance(node.lvalue, c_ast.UnaryOp):
                var = self.generator.visit(node.lvalue)
                if isinstance(node.lvalue, c_ast.ID) and (node.lvalue.name not in self.output_variables):  # Variável normal
                    self.components_outputs[func_name].append(var)
                elif isinstance(node.lvalue, c_ast.UnaryOp) and node.lvalue.op == '&' and (node.lvalue not in self.output_variables):  # Ponteiro
                    pointed_var = self.generator.visit(node.lvalue.expr)
                    self.components_outputs[func_name].append(pointed_var)
                elif (var in self.output_variables):
                    self.components_outputs[func_name].append(var)                
                elif (self.generator.visit(node.lvalue.expr) in self.output_variables):
                    self.components_outputs[func_name].append(self.generator.visit(node.lvalue.expr))   

            # Log em JSON após a chamada da função
            execution_order_str = f'{self.execution_order}'
            self.execution_order += 1

            args_in_json = [f'\\"{key}\\": \\"{c_type_to_printf.get(self.variables.get(key))}\\"' for key in self.components_inputs.get(func_name)]
            json_entry_before_call = r'"'+(
            f'{{\\"function\\": \\"{func_name}\\", '
            f'\\"executionOrder\\": \\"{execution_order_str}\\", '
            f'\\"in\\": {{{",".join(args_in_json)}}}'
            ) + r',"'
            args_before_call = ','.join([f'{key}' for key in self.components_inputs.get(func_name)])
            
            new_statements.append(c_ast.FuncCall(
                c_ast.ID("sprintf"),
                c_ast.ExprList([
                    c_ast.BinaryOp('+', c_ast.ID("log_buffer"), c_ast.FuncCall(c_ast.ID("strlen"), c_ast.ExprList([c_ast.ID("log_buffer")]))),
                    c_ast.Constant(type="string", value=json_entry_before_call + ','+ args_before_call)
                ])
            ))

            # Chamada da função original
            new_statements.append(node)
            
            args_out_json = [f'\\"{key}\\": \\"{c_type_to_printf.get(self.variables.get(key))}\\"' for key in self.components_outputs.get(func_name)]
            json_entry_after_call = r'"'+(
            f'\\"out\\": {{{",".join(args_out_json)}}}'
            ) + r'},", '
            args_after_call = ','.join(
                [f'*{key}' if key in self.output_variables else key for key in self.components_outputs.get(func_name)]
                )
            
            # Adicionar o sprintf direto para registrar no log_buffer acumulativamente
            new_statements.append(c_ast.FuncCall(
                c_ast.ID("sprintf"),
                c_ast.ExprList([
                    c_ast.BinaryOp('+', c_ast.ID("log_buffer"), c_ast.FuncCall(c_ast.ID("strlen"), c_ast.ExprList([c_ast.ID("log_buffer")]))),
                    c_ast.Constant(type="string", value=json_entry_after_call + args_after_call)
                ])
            ))

            return new_statements

        return node

    def generic_visit(self, node):
        new_block_items = []

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
        
def Create_Instrumented_Code(ast, function_name, bufferLength):
    try:
        adicionar_ao_log("Starting code instrumentation...")

        # Crie o injetor e aplique ao AST
        injector = FuncCallVisitor(function_name)
        injector.build_sut_variables_and_outputs(ast, function_name)
        injector.visit(ast)

        # Gere o código C com a injeção
        ast_to_instrument = copy.deepcopy(ast)
        generator = c_generator.CGenerator()
        instrumented_code = generator.visit(ast_to_instrument)
        
        # Adiciona cabeçalho para log_buffer e sprintf
        header = f'#include <stdio.h>\n#include <string.h>\n#include "instrumented_SUT.h"\nextern char log_buffer[{bufferLength}];\n'
        instrumented_code_with_header = header + instrumented_code

        # Escreva o código instrumentado em um novo arquivo
        instrumented_code_path = 'output\InstrumentedSUT\instrumented_SUT.c'
        with open(instrumented_code_path, 'w') as f:
            f.write(instrumented_code_with_header)

        gerar_arquivo_h_com_pycparser(ast)

        adicionar_ao_log("Instrumentation completed.")
        return instrumented_code_path
    except:
        error = f"ERROR: Instrumentation not executed properly." # {e.stderr}
        raise Exception(error)
    
    
if __name__ == '__main__':

    # Defina o nome do arquivo .c do SUT
    SUT_path = "examples\sut_final\sut.c" 

    # Defina o nome do arquivo .c do SUT
    folder_path = "examples\sut_final" 

    # Defina o nome da função testada
    function_name = "sut"

    bufferLength = 4096
    
    # Parsing do código C
    cpp_args = ['-E'] 
    ast = parse_file(SUT_path, use_cpp=True, cpp_path='gcc', cpp_args= cpp_args)

    Create_Instrumented_Code(ast, function_name, bufferLength)