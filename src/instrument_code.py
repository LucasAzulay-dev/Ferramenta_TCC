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
    'float': '%.3f',
    'double': '%.3lf',
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
        self.components_all_parameters = {}
        self.components_not_used_variables = {}
        
    def build_sut_variables_and_outputs(self, ast, target_function):
        nameInputsOutputs = ParseVariablesAndSutOutputs(ast, target_function)
        self.variables = nameInputsOutputs[0]
        self.output_variables = nameInputsOutputs[1]
        
    def visit_FuncDef(self, node):
		# Verificar se estamos na definição da função SUT
        function_name = node.decl.name
        if function_name == self.func_name:
            self.instrument_sut = True
            self.generic_visit(node)
            #print(self.variables)
            self.instrument_sut = False
        else:
            inputs, outputs, all_parameters = get_component_input_outputs(function_name, node)
            self.components_inputs[function_name] = inputs
            self.components_outputs[function_name] = outputs
            self.components_all_parameters[function_name] = all_parameters
            components_not_used_variables = [
                param for param in all_parameters if param not in inputs and param not in outputs
            ]
            self.components_not_used_variables[function_name] = components_not_used_variables

    def visit_FuncCall(self, node):
        if self.instrument_sut:
            func_name = self.generator.visit(node.name)
            if(func_name != 'sprintf'):
                new_statements = []
                #Ordered
                passed_parameters = []
                
                for arg in node.args.exprs:
                    var = self.generator.visit(arg)
                    if isinstance(arg, c_ast.ID) and (var not in self.output_variables):  # Variável normal
                        passed_parameters.append(var)
                    elif isinstance(arg, c_ast.UnaryOp) and arg.op == '&' and (var not in self.output_variables):  # Ponteiro
                        pointed_var = self.generator.visit(arg.expr)
                        passed_parameters.append(pointed_var)
                    elif (var in self.output_variables):
                        passed_parameters.append(var)
                
                component_all_params = self.components_all_parameters.get(func_name)
                
                for index, passed_parameter in enumerate(passed_parameters): 
                    # Obter o parâmetro da definição correspondente ao índice
                    param_def_to_change = component_all_params[index]
                    
                    not_used_vars = self.components_not_used_variables.get(func_name, [])
                    inputs = self.components_inputs.get(func_name, [])
                    outputs = self.components_outputs.get(func_name, [])

                    if param_def_to_change in not_used_vars:
                        not_used_vars[not_used_vars.index(param_def_to_change)] = passed_parameter
                    
                    if param_def_to_change in inputs:
                        inputs[inputs.index(param_def_to_change)] = passed_parameter
                    
                    if param_def_to_change in outputs:
                        outputs[outputs.index(param_def_to_change)] = passed_parameter

                    # Atualizar os dicionários com os novos valores
                    self.components_not_used_variables[func_name] = not_used_vars
                    self.components_inputs[func_name] = inputs
                    self.components_outputs[func_name] = outputs

                # Adicionar sprintf para registrar dados em JSON após a função
                execution_order_str = f'{self.execution_order}'
                self.execution_order += 1

                args_not_used = [f'\\"{key}\\": \\"{c_type_to_printf.get(self.variables.get(key))}\\"' for key in self.components_not_used_variables.get(func_name)]
                args_in_json = [f'\\"{key}\\": \\"{c_type_to_printf.get(self.variables.get(key))}\\"' for key in self.components_inputs.get(func_name)]
                json_entry_before_call = r'"'+(
                f'{{\\"function\\": \\"{func_name}\\", '
                f'\\"executionOrder\\": \\"{execution_order_str}\\", '
                f'\\"not_used\\": {{{",".join(args_not_used)}}},'
                f'\\"in\\": {{{",".join(args_in_json)}}}'
                ) + r',"'
                args_not_used = ','.join([f'{key}' for key in self.components_not_used_variables.get(func_name)])
                args_before_call = ','.join([f'{key}' for key in self.components_inputs.get(func_name)])
                args_combined = ','.join(
                filter(None, [args_not_used, args_before_call])
                )
                
                new_statements.append(c_ast.FuncCall(
                    c_ast.ID("sprintf"),
                    c_ast.ExprList([
                        c_ast.BinaryOp('+', c_ast.ID("log_buffer"), c_ast.FuncCall(c_ast.ID("strlen"), c_ast.ExprList([c_ast.ID("log_buffer")]))),
                        c_ast.Constant(type="string", value=json_entry_before_call + ', '+ args_combined)
                    ])
                ))

                # Chamada da função original
                new_statements.append(node)
                
                args_out_json = [f'\\"{key}\\": \\"{c_type_to_printf.get(self.variables.get(key))}\\"' for key in self.components_outputs.get(func_name)]
                json_entry_after_call = r'"'+(
                f'\\"out\\": {{{",".join(args_out_json)}}}'
                ) + r'},", '
                args_after_call = ','.join(
                [f'{self.output_variables.get(key)}{key}' if key in self.output_variables.keys() else key for key in self.components_outputs.get(func_name)]
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
            passed_parameters = []
            
            for arg in func_call.args.exprs:
                    var = self.generator.visit(arg)
                    if isinstance(arg, c_ast.ID) and (var not in self.output_variables):  # Variável normal
                        passed_parameters.append(var)
                    elif isinstance(arg, c_ast.UnaryOp) and arg.op == '&' and (var not in self.output_variables):  # Ponteiro
                        pointed_var = self.generator.visit(arg.expr)
                        passed_parameters.append(pointed_var)
                    elif (var in self.output_variables):
                        passed_parameters.append(var)
                        
            component_all_params = self.components_all_parameters.get(func_name)
                
            for index, passed_parameter in enumerate(passed_parameters): 
                # Obter o parâmetro da definição correspondente ao índice
                param_def_to_change = component_all_params[index]
                
                not_used_vars = self.components_not_used_variables.get(func_name, [])
                inputs = self.components_inputs.get(func_name, [])
                outputs = self.components_outputs.get(func_name, [])

                if param_def_to_change in not_used_vars:
                    not_used_vars[not_used_vars.index(param_def_to_change)] = passed_parameter
                
                if param_def_to_change in inputs:
                    inputs[inputs.index(param_def_to_change)] = passed_parameter
                
                if param_def_to_change in outputs:
                    outputs[outputs.index(param_def_to_change)] = passed_parameter

                # Atualizar os dicionários com os novos valores
                self.components_not_used_variables[func_name] = not_used_vars
                self.components_inputs[func_name] = inputs
                self.components_outputs[func_name] = outputs

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

            args_not_used = [f'\\"{key}\\": \\"{c_type_to_printf.get(self.variables.get(key))}\\"' for key in self.components_not_used_variables.get(func_name)]
            args_in_json = [f'\\"{key}\\": \\"{c_type_to_printf.get(self.variables.get(key))}\\"' for key in self.components_inputs.get(func_name)]
            json_entry_before_call = r'"'+(
            f'{{\\"function\\": \\"{func_name}\\", '
            f'\\"executionOrder\\": \\"{execution_order_str}\\", '
            f'\\"not_used\\": {{{",".join(args_not_used)}}},'
            f'\\"in\\": {{{",".join(args_in_json)}}}'
            ) + r',"'
            args_not_used = ','.join([f'{key}' for key in self.components_not_used_variables.get(func_name)])
            args_before_call = ','.join([f'{key}' for key in self.components_inputs.get(func_name)])
            args_combined = ','.join(
                filter(None, [args_not_used, args_before_call])
            )
            
            new_statements.append(c_ast.FuncCall(
                c_ast.ID("sprintf"),
                c_ast.ExprList([
                    c_ast.BinaryOp('+', c_ast.ID("log_buffer"), c_ast.FuncCall(c_ast.ID("strlen"), c_ast.ExprList([c_ast.ID("log_buffer")]))),
                    c_ast.Constant(type="string", value=json_entry_before_call + ', '+ args_combined)
                ])
            ))

            # Chamada da função original
            new_statements.append(node)
            
            args_out_json = [f'\\"{key}\\": \\"{c_type_to_printf.get(self.variables.get(key))}\\"' for key in self.components_outputs.get(func_name)]
            json_entry_after_call = r'"'+(
            f'\\"out\\": {{{",".join(args_out_json)}}}'
            ) + r'},", '
            args_after_call = ','.join(
            [f'{self.output_variables.get(key)}{key}' if key in self.output_variables.keys() else key for key in self.components_outputs.get(func_name)]
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
    # SUT_path = "examples\C_proj_mockup_2\SUT\SUT.c" 

    # Defina o nome da função testada
    function_name = "sut"
    # function_name = "SUT"

    bufferLength = 4096
    
    # Parsing do código C
    ast = generate_ast(SUT_path)

    Create_Instrumented_Code(ast, function_name, bufferLength)