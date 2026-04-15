# semantic.py
from ast_nodes import *

class SemanticAnalyzer:
    def __init__(self):
        # A nossa Tabela de Símbolos: guarda o nome da variável e o seu tipo
        # Exemplo: {'NUM': 'INTEGER', 'ISPRIM': 'LOGICAL'}
        self.symbol_table = {}
        self.errors = []

    def analyze(self, ast):
        self.visit(ast)
        return self.errors

    def visit(self, node):
        if node is None:
            return None
        # Chama automaticamente a função certa para cada tipo de nó
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # Para nós que não precisam de verificação específica, tentamos visitar os filhos
        if hasattr(node, '__dict__'):
            for value in node.__dict__.values():
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, Node):
                            self.visit(item)
                elif isinstance(value, Node):
                    self.visit(value)

    # --- 1. PROGRAMA PRINCIPAL ---
    def visit_ProgramNode(self, node):
        # Primeiro verificamos as declarações explícitas
        for decl in node.decls:
            self.visit(decl)
        # Depois verificamos o corpo do programa
        for stmt in node.body:
            self.visit(stmt)

    # --- 2. DECLARAÇÕES EXPLÍCITAS (Guardar na Tabela de Símbolos) ---
    def visit_VarDeclNode(self, node):
        if node.name in self.symbol_table:
            self.errors.append(f"❌ Erro Semântico: A variável '{node.name}' já foi declarada.")
        else:
            self.symbol_table[node.name] = node.type

    # --- NOVA REGRA DO FORTRAN: TIPAGEM IMPLÍCITA ---
    def get_implicit_type(self, var_name):
        # Se a variável não estiver declarada, o Fortran adivinha pelo nome!
        if var_name not in self.symbol_table:
            primeira_letra = var_name[0].upper()
            if primeira_letra in 'IJKLMN':
                self.symbol_table[var_name] = 'INTEGER'
            else:
                self.symbol_table[var_name] = 'REAL'
        return self.symbol_table[var_name]

    # --- 3. ATRIBUIÇÕES E VARIÁVEIS ---
    def visit_VarNode(self, node):
        return self.get_implicit_type(node.name)

    def visit_AssignNode(self, node):
        # Vai buscar o tipo da variável (ou infere-o implicitamente)
        var_type = self.get_implicit_type(node.var)

        # Vai buscar o tipo da expressão
        expr_type = self.visit(node.expr)

        # Validação simples: não misturar LOGICAL com INTEGER/REAL
        if expr_type and expr_type != 'UNKNOWN':
            if var_type == 'LOGICAL' and expr_type != 'LOGICAL':
                self.errors.append(f"❌ Erro Semântico: Tentativa de guardar um {expr_type} na variável '{node.var}' (que é {var_type}).")
            elif var_type in ['INTEGER', 'REAL'] and expr_type == 'LOGICAL':
                self.errors.append(f"❌ Erro Semântico: Tentativa de guardar um LOGICAL na variável numérica '{node.var}'.")

    def visit_ReadNode(self, node):
        # Inferir tipo se a variável for lida logo diretamente sem declaração
        self.get_implicit_type(node.var)

    # --- 4. EXPRESSÕES MATEMÁTICAS E LÓGICAS ---
    def visit_LiteralNode(self, node):
        if isinstance(node.value, bool):
            return 'LOGICAL'
        elif isinstance(node.value, float):
            return 'REAL'
        else:
            return 'INTEGER'

    def visit_BinOpNode(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type == 'UNKNOWN' or right_type == 'UNKNOWN':
            return 'UNKNOWN'

        ops_aritmeticas = ['+', '-', '*', '/']
        ops_relacionais = ['.EQ.', '.NE.', '.LT.', '.LE.', '.GT.', '.GE.']
        ops_logicas = ['.AND.', '.OR.']

        if node.op in ops_aritmeticas:
            if left_type == 'LOGICAL' or right_type == 'LOGICAL':
                self.errors.append(f"❌ Erro Semântico: Operação matemática '{node.op}' não pode ser usada com valores lógicos.")
            return 'INTEGER' if left_type == 'INTEGER' and right_type == 'INTEGER' else 'REAL'

        elif node.op in ops_relacionais:
            if left_type == 'LOGICAL' or right_type == 'LOGICAL':
                self.errors.append(f"❌ Erro Semântico: Operação de comparação '{node.op}' exige números.")
            return 'LOGICAL'

        elif node.op in ops_logicas:
            if left_type != 'LOGICAL' or right_type != 'LOGICAL':
                self.errors.append(f"❌ Erro Semântico: Operação lógica '{node.op}' exige valores booleanos (.TRUE. ou .FALSE.).")
            return 'LOGICAL'

    def visit_IfNode(self, node):
        cond_type = self.visit(node.condition)
        if cond_type and cond_type != 'LOGICAL' and cond_type != 'UNKNOWN':
            self.errors.append(f"❌ Erro Semântico: A condição do IF deve ser um valor LOGICO, mas recebemos um {cond_type}.")
        
        # Visita os blocos internos
        for stmt in node.then_block:
            self.visit(stmt)
        if node.else_block:
            for stmt in node.else_block:
                self.visit(stmt)