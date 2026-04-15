# compiler.py
import re
from ast_nodes import *

class Compiler:
    def __init__(self, symbol_table=None):
        self.instructions = []
        self.var_info = {} 
        self.next_addr = 0
        self.subroutines = {}
        self.if_counter = 0
        self.do_loops = {}

        if symbol_table:
            for var_name, info in symbol_table.items():
                self._register_var(var_name, info)

    def _parse_name_size(self, text):
        text = str(text)
        base_name = text.split('(')[0].split('[')[0].strip().upper()
        match = re.search(r'[\[\(](\d+)[\]\)]', text)
        size = int(match.group(1)) if match else 1
        return base_name, size

    def _register_var(self, name, info=None):
        b1, s1 = self._parse_name_size(name)
        s2 = self._parse_name_size(info)[1] if info else 1
        size = max(s1, s2)
        
        if b1 not in self.var_info:
            self.var_info[b1] = {'addr': self.next_addr, 'size': size}
            self.next_addr += 1
        else:
            self.var_info[b1]['size'] = max(self.var_info[b1]['size'], size)
        return self.var_info[b1]

    def _info(self, name):
        b, s = self._parse_name_size(name)
        if b not in self.var_info:
            self.var_info[b] = {'addr': self.next_addr, 'size': s}
            self.next_addr += 1
        return self.var_info[b]

    def _extract_name(self, obj):
        if hasattr(obj, 'name'): return self._parse_name_size(obj.name)[0]
        if hasattr(obj, 'var'): return self._parse_name_size(obj.var)[0]
        return self._parse_name_size(obj)[0]

    def emit(self, ins, comm=""):
        if comm: self.instructions.append(f"// {comm}")
        self.instructions.append(ins)

    def compile(self, ast):
        # A MAGIA ESTÁ AQUI: 3 PASSOS RASTREADORES
        self.register_subs(ast) # Passo 1: Descobre todas as Funções
        self.pre_pass(ast)      # Passo 2: Caça os falsos Arrays
        self.visit(ast)         # Passo 3: Gera o Código EWVM
        return self.instructions

    # --- NOVO: LÊ AS FUNÇÕES ANTES DE TUDO O RESTO ---
    def register_subs(self, node):
        if node is None: return
        if node.__class__.__name__ == 'SubroutineNode':
            self.subroutines[self._extract_name(node.name)] = getattr(node, 'params', [])
        if hasattr(node, '__dict__'):
            for v in node.__dict__.values():
                if isinstance(v, list):
                    for i in v:
                        if isinstance(i, Node): self.register_subs(i)
                elif isinstance(v, Node): self.register_subs(v)

    def pre_pass(self, node):
        if node is None: return
        t = node.__class__.__name__
            
        if t == 'VarDeclNode':
            info = self._register_var(node.name)
            if hasattr(node, 'size') and node.size:
                info['size'] = max(info['size'], int(node.size))
                
        elif t == 'CallNode':
            base_name = self._extract_name(node)
            if base_name != 'MOD' and base_name not in self.subroutines:
                info = self._info(base_name)
                if info['size'] == 1: info['size'] = 50
                
        elif t in ['ReadNode', 'AssignNode']:
            var_node = getattr(node, 'var', None)
            if var_node and var_node.__class__.__name__ == 'CallNode':
                base_name = self._extract_name(var_node)
                # Só diz que é array se NÃO for uma função já registada!
                if base_name != 'MOD' and base_name not in self.subroutines:
                    info = self._info(base_name)
                    if info['size'] == 1: info['size'] = 50

        if hasattr(node, '__dict__'):
            for v in node.__dict__.values():
                if isinstance(v, list):
                    for i in v:
                        if isinstance(i, Node): self.pre_pass(i)
                elif isinstance(v, Node): self.pre_pass(v)

    def visit(self, node):
        if node is None: return
        method = getattr(self, f'visit_{node.__class__.__name__}', self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        if hasattr(node, '__dict__'):
            for v in node.__dict__.values():
                if isinstance(v, list):
                    for i in v:
                        if isinstance(i, Node): self.visit(i)
                elif isinstance(v, Node): self.visit(v)

    # --- 1. PROGRAMA PRINCIPAL ---
    def visit_ProgramNode(self, node):
        self.emit("", "--- DECLARACAO DE ESPACO NA PILHA ---")
        for name, info in sorted(self.var_info.items(), key=lambda x: x[1]['addr']):
            self.emit("pushi 0", f"Reserva gp[{info['addr']}] para '{name}'")
            
        self.emit("", "--- INICIALIZACAO DE ARRAYS ---")
        for name, info in sorted(self.var_info.items(), key=lambda x: x[1]['addr']):
            if info['size'] > 1:
                self.emit(f"alloc {info['size']}", f"Aloca Array '{name}'")
                self.emit(f"storeg {info['addr']}")

        self.emit("\nstart")
        for stmt in node.body:
            if getattr(stmt, 'label', None): self.emit(f"L{stmt.label}:")
            self.visit(stmt)
        self.emit("stop")

        if getattr(node, 'subprograms', None):
            self.emit("\n// --- SUBPROGRAMAS ---")
            for sub in node.subprograms: self.visit(sub)

    # --- 2. VALORES E VARIÁVEIS ---
    def visit_LiteralNode(self, node):
        val = 1 if node.value is True else (0 if node.value is False else node.value)
        self.emit(f"pushi {val}")

    def visit_VarNode(self, node):
        info = self._info(node.name)
        self.emit(f"pushg {info['addr']}", f"Ler {self._extract_name(node)}")
        if getattr(node, 'index', None):
            self.visit(node.index)
            self.emit("pushi 1"); self.emit("sub"); self.emit("loadn")

    # --- 3. ATRIBUIÇÕES ---
    def visit_AssignNode(self, node):
        is_array_call = hasattr(node, 'var') and hasattr(node.var, '__class__') and node.var.__class__.__name__ == 'CallNode'
        
        if is_array_call:
            base_name = self._extract_name(node.var)
            info = self._info(base_name)
            self.emit(f"pushg {info['addr']}", f"Address array {base_name}")
            self.visit(node.var.args[0])
            self.emit("pushi 1"); self.emit("sub")
            self.visit(node.expr)
            self.emit("storen")
        elif getattr(node, 'index', None):
            base_name = self._extract_name(node.var)
            info = self._info(base_name)
            self.emit(f"pushg {info['addr']}", f"Address array {base_name}")
            self.visit(node.index)
            self.emit("pushi 1"); self.emit("sub")
            self.visit(node.expr)
            self.emit("storen")
        else:
            base_name = self._extract_name(node.var)
            info = self._info(base_name)
            self.visit(node.expr)
            self.emit(f"storeg {info['addr']}", f"Guardar {base_name}")

    def visit_ArrayAssignNode(self, node):
        base_name = self._extract_name(node.name)
        info = self._info(base_name)
        self.emit(f"pushg {info['addr']}", f"Address array {base_name}")
        self.visit(node.index)
        self.emit("pushi 1"); self.emit("sub")
        self.visit(node.expr)
        self.emit("storen")

    # --- 4. I/O ---
    def visit_ReadNode(self, node):
        is_array_call = hasattr(node, 'var') and hasattr(node.var, '__class__') and node.var.__class__.__name__ == 'CallNode'
        
        if is_array_call:
            base_name = self._extract_name(node.var)
            info = self._info(base_name)
            self.emit(f"pushg {info['addr']}", f"Address array {base_name}")
            self.visit(node.var.args[0])
            self.emit("pushi 1"); self.emit("sub")
            self.emit("read")
            self.emit("atoi")
            self.emit("storen")
        elif getattr(node, 'index', None):
            base_name = self._extract_name(getattr(node, 'var', getattr(node, 'name', '')))
            info = self._info(base_name)
            self.emit(f"pushg {info['addr']}")
            self.visit(node.index)
            self.emit("pushi 1"); self.emit("sub")
            self.emit("read")
            self.emit("atoi")
            self.emit("storen")
        else:
            base_name = self._extract_name(getattr(node, 'var', getattr(node, 'name', '')))
            info = self._info(base_name)
            self.emit("read")
            self.emit("atoi")
            self.emit(f"storeg {info['addr']}", f"Guardar {base_name}")

    # --- 5. OPERAÇÕES ---
    def visit_BinOpNode(self, node):
        self.visit(node.left)
        self.visit(node.right)
        op = node.op.upper()
        map_op = {'+':'add','-':'sub','*':'mul','/':'div','.EQ.':'equal','.LT.':'inf','.LE.':'infeq','.GT.':'sup','.GE.':'supeq','.AND.':'and','.OR.':'or'}
        if op == '.NE.':
            self.emit('equal'); self.emit('not')
        else:
            self.emit(map_op.get(op, "nop"))

    def visit_UnaryOpNode(self, node):
        self.visit(node.expr)
        self.emit("not")

    def visit_PrintNode(self, node):
        for e in node.elements:
            if isinstance(e, str):
                self.emit(f'pushs "{e}"'); self.emit("writes")
            else:
                self.visit(e); self.emit("writei")
        self.emit("writeln")

    # --- 6. FLUXO ---
    def visit_IfNode(self, node):
        c = self.if_counter; self.if_counter += 1
        self.visit(node.condition); self.emit(f"jz ELSE{c}")
        for s in node.then_block: self.visit(s)
        self.emit(f"jump ENDIF{c}\nELSE{c}:")
        if node.else_block:
            for s in node.else_block: self.visit(s)
        self.emit(f"ENDIF{c}:")

    def visit_DoNode(self, node):
        info = self._info(node.var)
        self.do_loops[node.label_ref] = {'addr': info['addr'], 'var': self._extract_name(node.var)}
        self.visit(node.start); self.emit(f"storeg {info['addr']}")
        self.emit(f"DOSTART{node.label_ref}:")
        self.emit(f"pushg {info['addr']}")
        self.visit(node.end); self.emit("sup"); self.emit("not")
        self.emit(f"jz DOEND{node.label_ref}")

    def visit_ContinueNode(self, node):
        lab = getattr(node, 'label', None)
        if lab in self.do_loops:
            d = self.do_loops[lab]
            self.emit(f"pushg {d['addr']}"); self.emit("pushi 1"); self.emit("add"); self.emit(f"storeg {d['addr']}")
            self.emit(f"jump DOSTART{lab}\nDOEND{lab}:")
        else:
            self.emit("nop")

    def visit_GotoNode(self, node):
        self.emit(f"jump L{node.target}")

# --- 7. A MAGIA FINAL DO CALLNODE ---
    def visit_CallNode(self, node):
        base_name = self._extract_name(node)
        if base_name == 'MOD' and len(node.args) == 2:
            self.visit(node.args[0]); self.visit(node.args[1]); self.emit("mod")
        else:
            info = self._info(base_name)
            if info['size'] > 1 or base_name not in self.subroutines:
                self.emit(f"pushg {info['addr']}", f"Ler array {base_name}")
                self.visit(node.args[0])
                self.emit("pushi 1"); self.emit("sub")
                self.emit("loadn")
            else:
                # O SEGREDO RECUPERADO: Passar os argumentos para os parâmetros!
                params = self.subroutines[base_name]
                for arg, param_name in zip(node.args, params):
                    self.visit(arg) # Avalia o argumento (ex: NUM)
                    param_info = self._info(param_name)
                    self.emit(f"storeg {param_info['addr']}", f"Argumento -> {param_name}")
                
                self.emit(f"pusha {node.name}")
                self.emit("call")
                
                if base_name in self.var_info:
                    self.emit(f"pushg {info['addr']}", f"Retorno de {base_name}")

    def visit_SubroutineNode(self, node):
        self.emit(f"\n{node.name}:")
        for s in node.body:
            # IMPRIME A LABEL NA FUNÇÃO! (Corrige o Grammar Error L20)
            if getattr(s, 'label', None): self.emit(f"L{s.label}:")
            self.visit(s)

    def visit_ReturnNode(self, node):
        self.emit("return")