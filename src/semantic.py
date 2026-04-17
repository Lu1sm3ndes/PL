# semantic.py
from ast_nodes import *

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.arrays = set()          # NOVO: Guarda nomes de Arrays
        self.subroutines = set()     # NOVO: Guarda nomes de funções
        self.errors = []
        self.warnings = []           # NOVO: Guarda os avisos de inicialização
        self.initialized_vars = set()# NOVO: Variáveis que já têm valor

    def _extract_name(self, name):
        # Limpa "[5]" ou "(I)" para ficarmos só com o nome base
        return str(name).split('[')[0].split('(')[0].strip().upper()

    def analyze(self, ast):
        self.visit(ast)
        return self.errors, self.warnings # Modificado para devolver avisos

    def visit(self, node):
        if node is None: return None
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if hasattr(node, '__dict__'):
            for value in node.__dict__.values():
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, Node): self.visit(item)
                elif isinstance(value, Node):
                    self.visit(value)

    # --- 1. PROGRAMA PRINCIPAL ---
    def visit_ProgramNode(self, node):
        # 1. Regista os nomes das Subrotinas primeiro!
        for sub in getattr(node, 'subprograms', []):
            self.subroutines.add(self._extract_name(sub.name))
        for decl in node.decls: self.visit(decl)
        for stmt in node.body: self.visit(stmt)
        for sub in getattr(node, 'subprograms', []): self.visit(sub)

    # --- 2. DECLARAÇÕES ---
    def visit_VarDeclNode(self, node):
        base_name = self._extract_name(node.name)
        if base_name in self.symbol_table:
            self.errors.append(f"❌ Erro Semântico: A variável '{base_name}' já foi declarada.")
        else:
            self.symbol_table[base_name] = node.type
            # Se a string original tiver parenteses/parêntesis retos, é array!
            if '[' in str(node.name) or '(' in str(node.name):
                self.arrays.add(base_name)

    def get_implicit_type(self, var_name):
        base_name = self._extract_name(var_name)
        if base_name not in self.symbol_table:
            primeira_letra = base_name[0].upper()
            if primeira_letra in 'IJKLMN': self.symbol_table[base_name] = 'INTEGER'
            else: self.symbol_table[base_name] = 'REAL'
        return self.symbol_table[base_name]

    # --- 3. ATRIBUIÇÕES E VARIÁVEIS ---
    def visit_VarNode(self, node):
        base_name = self._extract_name(node.name)
        # DETEÇÃO DE VARIÁVEL VAZIA!
        if base_name not in self.initialized_vars and base_name not in self.arrays:
            self.warnings.append(f"⚠️ Aviso: A variável '{base_name}' está a ser usada sem ter sido inicializada.")
        return self.get_implicit_type(base_name)

    def visit_AssignNode(self, node):
        base_name = self._extract_name(node.var)
        self.initialized_vars.add(base_name) # Marca como inicializada
        
        var_type = self.get_implicit_type(base_name)
        expr_type = self.visit(node.expr)

        if expr_type and expr_type != 'UNKNOWN':
            if var_type == 'LOGICAL' and expr_type != 'LOGICAL':
                self.errors.append(f"❌ Erro Semântico: Tentativa de guardar um {expr_type} na variável '{base_name}' (que é {var_type}).")
            elif var_type in ['INTEGER', 'REAL'] and expr_type == 'LOGICAL':
                self.errors.append(f"❌ Erro Semântico: Tentativa de guardar LOGICAL na variável numérica '{base_name}'.")

    def visit_ArrayAssignNode(self, node):
        base_name = self._extract_name(node.name)
        self.initialized_vars.add(base_name)
        
        # O POLÍCIA VOLTOU!
        if base_name not in self.arrays:
            self.errors.append(f"❌ Erro Semântico: Tentativa de indexar '{base_name}', que é uma variável escalar de tamanho 1.")
            
        self.visit(node.index)
        self.visit(node.expr)

    def visit_CallNode(self, node):
        base_name = self._extract_name(node.name)
        
        if base_name != 'MOD' and base_name not in self.subroutines:
            # O POLÍCIA VOLTOU!
            if base_name not in self.arrays:
                self.errors.append(f"❌ Erro Semântico: Tentativa de indexar '{base_name}', que é uma variável escalar.")
            if base_name not in self.initialized_vars:
                self.warnings.append(f"⚠️ Aviso: Acesso ao array '{base_name}' que poderá não estar inicializado.")
            return self.get_implicit_type(base_name)
            
        for arg in getattr(node, 'args', []): self.visit(arg)
        return 'INTEGER'

    def visit_ReadNode(self, node):
        base_name = self._extract_name(getattr(node, 'var', getattr(node, 'name', '')))
        self.initialized_vars.add(base_name) # Marca como inicializada
        self.get_implicit_type(base_name)

    def visit_DoNode(self, node):
        # O ciclo DO dá o valor inicial à variável de controlo!
        base_name = self._extract_name(node.var)
        self.initialized_vars.add(base_name)
        
        # Visita o valor de início e de fim para garantir que não há erros neles
        self.visit(node.start)
        self.visit(node.end)

    def visit_SubroutineNode(self, node):
        # Os parâmetros da função já vêm preenchidos "de fora", logo marcamos como inicializados
        for p in node.params:
            self.initialized_vars.add(self._extract_name(p))
        for decl in node.decls: self.visit(decl)
        for stmt in node.body: self.visit(stmt)

    # ... (Podes manter as tuas visit_LiteralNode, visit_BinOpNode e visit_IfNode iguaizinhas ao que já tinhas) ...
    def visit_LiteralNode(self, node):
        if isinstance(node.value, bool): return 'LOGICAL'
        elif isinstance(node.value, float): return 'REAL'
        else: return 'INTEGER'

    def visit_BinOpNode(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type == 'UNKNOWN' or right_type == 'UNKNOWN': return 'UNKNOWN'
        if node.op in ['+', '-', '*', '/']: return 'INTEGER' if left_type == 'INTEGER' and right_type == 'INTEGER' else 'REAL'
        elif node.op in ['.EQ.', '.NE.', '.LT.', '.LE.', '.GT.', '.GE.', '.AND.', '.OR.']: return 'LOGICAL'

    def visit_IfNode(self, node):
        self.visit(node.condition)
        for stmt in node.then_block: self.visit(stmt)
        if node.else_block:
            for stmt in node.else_block: self.visit(stmt)