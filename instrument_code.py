from pycparser import c_ast, c_generator, parse_file

class FuncCallVisitor(c_ast.NodeVisitor):
	def __init__(self):
		self.generator = c_generator.CGenerator()
		self.instrument_sut = False  # Para controlar se estamos dentro de SUT
		self.output_variables = []

	def visit_FuncDef(self, node):
		# Verificar se estamos na definição da função SUT
		if node.decl.name == "SUT":
			self.instrument_sut = True
			self.generic_visit(node)
			self.instrument_sut = False
		else:
			# Ignorar outras funções
			pass

	def visit_FuncCall(self, node):
		if self.instrument_sut:
			func_name = self.generator.visit(node.name)
			new_statements = []

			# Gerar os argumentos e os printf
			args_before = []
			args_after = []
			args_list_before = []
			args_list_after = []

			for arg in node.args.exprs:
				arg_code = self.generator.visit(arg)
				if isinstance(arg, c_ast.ID) and (arg_code not in self.output_variables):  # Variável normal
					args_before.append(f"{arg_code}:%d")
					args_list_before.append(arg_code)
				elif isinstance(arg, c_ast.UnaryOp) and arg.op == '&' and (arg_code not in self.output_variables):  # Argumento ponteiro
					pointed_var = self.generator.visit(arg.expr)
					args_after.append(f"{pointed_var}:%d")
					args_list_after.append(pointed_var)

			# Adicionar printf antes da função para valores iniciais
			if args_before:
				printf_before_code = f'"{func_name}_return_variables_and_initial_values: [{{' + ', '.join(args_before) + '}}]\\n", ' + ', '.join(args_list_before)
				printf_before = c_ast.FuncCall(c_ast.ID("printf"), c_ast.ExprList([c_ast.Constant(type="string", value=printf_before_code)]))
				new_statements.append(printf_before)

			# A chamada da função original
			new_statements.append(node)

			# Adicionar printf depois da função para valores finais
			if args_after:
				printf_after_code = f'"{func_name}_return_variables_and_final_values: [{{' + ', '.join(args_after) + '}}]\\n", ' + ', '.join(args_list_after)
				printf_after = c_ast.FuncCall(c_ast.ID("printf"), c_ast.ExprList([c_ast.Constant(type="string", value=printf_after_code)]))
				new_statements.append(printf_after)

			return new_statements
		else:
			# Se não estamos em SUT, retorna apenas o node original
			return node

	def visit_Assignment(self, node):
		# Instrumenta atribuições somente dentro de SUT
		if self.instrument_sut and isinstance(node.rvalue, c_ast.FuncCall):
			func_call = node.rvalue
			func_name = self.generator.visit(func_call.name)

			# Lista de novos statements
			new_statements = []

			# Gerar os argumentos para printf
			args_list = []
			for arg in func_call.args.exprs:
				arg_code = self.generator.visit(arg)
				if isinstance(arg, c_ast.ID) and (arg_code not in self.output_variables):  # Variável normal
					args_list.append(arg_code)
				elif isinstance(arg, c_ast.UnaryOp) and arg.op == '&' and (arg_code not in self.output_variables):  # Argumento ponteiro
					pointed_var = self.generator.visit(arg.expr)
					args_list.append(pointed_var)

			# Adicionar printf antes da atribuição
			printf_code = f'"{func_name}_return_variables_and_initial_values: [{{' + ', '.join([f"{arg}:%d" for arg in args_list]) + '}}]\\n", ' + ', '.join(args_list)
			printf_before = c_ast.FuncCall(c_ast.ID("printf"), c_ast.ExprList([c_ast.Constant(type="string", value=printf_code)]))
			new_statements.append(printf_before)

			# Adicionar a atribuição
			new_statements.append(node)

			# Adicionar printf depois da atribuição, focando no SUTO1 e SUTO2
			if isinstance(node.lvalue, c_ast.PtrDecl) or isinstance(node.lvalue, c_ast.ID):
				assigned_var = self.generator.visit(node.lvalue)
				printf_after_code = f'"{func_name}_return_variables_and_final_values: [{{{assigned_var}:%d}}]\\n", {assigned_var}'
				printf_after = c_ast.FuncCall(c_ast.ID("printf"), c_ast.ExprList([c_ast.Constant(type="string", value=printf_after_code)]))
				new_statements.append(printf_after)

			return new_statements

		# Para outros tipos de atribuição, apenas retorne o node
		return node

	def generic_visit(self, node):
		initial_sut_output_statements = []
		final_sut_output_statements = []
		new_block_items = []

		if self.instrument_sut and isinstance(node, c_ast.FuncDecl):
			# Captura as variáveis de saída se estamos no SUT
			for params in node.args.params:
				if isinstance(params.type, c_ast.PtrDecl):
					self.output_variables.append(params.name)

		if self.instrument_sut and isinstance(node, c_ast.Compound):
			# Processa os statements dentro do bloco da função SUT
			for stmt in (node.block_items or []):
				if isinstance(stmt, c_ast.FuncCall):
					# Instrumenta a chamada de funções
					instrumented_statements = self.visit_FuncCall(stmt)
					new_block_items.extend(instrumented_statements)
				elif isinstance(stmt, c_ast.Assignment):
					# Instrumenta atribuições
					instrumented_statements = self.visit_Assignment(stmt)
					new_block_items.extend(instrumented_statements)
				else:
					# Mantém outros statements
					new_block_items.append(stmt)
						# Adiciona as instrumentações de printf para os valores iniciais e finais
			if len(self.output_variables) != 0:
				print(self.output_variables)
				
				# Instrumentação inicial (valores iniciais das variáveis de saída)
				initial_sut_outputs = f'"sut_output_variables_and_initial_values: [{{' + ', '.join([f'{var}:%d' for var in self.output_variables]) + '}}]\\n", ' + ', '.join([f'*{var}' for var in self.output_variables])
				printf_initial_sut_outputs = c_ast.FuncCall(c_ast.ID("printf"), c_ast.ExprList([c_ast.Constant(type="string", value=initial_sut_outputs)]))
				initial_sut_output_statements.append(printf_initial_sut_outputs)
				
				# Instrumentação final (valores finais das variáveis de saída)
				final_sut_outputs = f'"sut_output_variables_and_final_values: [{{' + ', '.join([f'{var}:%d' for var in self.output_variables]) + '}}]\\n", ' + ', '.join([f'*{var}' for var in self.output_variables])
				printf_final_sut_outputs = c_ast.FuncCall(c_ast.ID("printf"), c_ast.ExprList([c_ast.Constant(type="string", value=final_sut_outputs)]))
				final_sut_output_statements.append(printf_final_sut_outputs)
				
				# Limpa a lista de variáveis de saída
				self.output_variables = []
			
			# Insere as instrumentações no início e no fim do bloco da função
		if len(initial_sut_output_statements) > 0:
				new_block_items = initial_sut_output_statements + new_block_items + final_sut_output_statements

				node.block_items = new_block_items


		super().generic_visit(node)


def Create_Instrumented_Code(code_path):
	# Parse o arquivo C'
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
	Create_Instrumented_Code(code_path)
