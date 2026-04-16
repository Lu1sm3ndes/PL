# optimizer.py
from ast_nodes import *

class Optimizer:
    def optimize(self, ast):
        return self.visit(ast)

    def visit(self, node):
        if node is None:
            return None
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Visita genérica que tenta otimizar todos os atributos do nó"""
        if hasattr(node, '__dict__'):
            for key, value in node.__dict__.items():
                if isinstance(value, list):
                    # Se for uma lista de instruções, otimiza cada uma e achata listas aninhadas
                    setattr(node, key, self.optimize_block(value))
                elif isinstance(value, Node):
                    # Se for um nó singular, substitui pelo nó otimizado
                    setattr(node, key, self.visit(value))
        return node

    def optimize_block(self, block):
        """Ajuda a processar listas de instruções (como o body do programa ou de um IF)"""
        new_block = []
        for stmt in block:
            opt_stmt = self.visit(stmt)
            # A eliminação de código morto pode devolver uma lista de instruções em vez de um nó único
            if isinstance(opt_stmt, list):
                new_block.extend(opt_stmt)
            elif opt_stmt is not None:
                new_block.append(opt_stmt)
        return new_block

    # --- 1. CONSTANT FOLDING ---
    def visit_BinOpNode(self, node):
        # 1. Tenta otimizar a esquerda e a direita primeiro (Bottom-Up)
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)

        # 2. Se a esquerda e a direita já forem números literais, fazemos a conta!
        if isinstance(node.left, LiteralNode) and isinstance(node.right, LiteralNode):
            v1 = node.left.value
            v2 = node.right.value
            op = node.op.upper()

            # Evitar crashar o compilador com divisões por zero
            try:
                if op == '+': return LiteralNode(v1 + v2)
                elif op == '-': return LiteralNode(v1 - v2)
                elif op == '*': return LiteralNode(v1 * v2)
                elif op == '/': return LiteralNode(int(v1 / v2)) # Força a ser um número inteiro
                elif op == '.EQ.': return LiteralNode(v1 == v2)
                elif op == '.NE.': return LiteralNode(v1 != v2)
                elif op == '.GT.': return LiteralNode(v1 > v2)
                elif op == '.LT.': return LiteralNode(v1 < v2)
                elif op == '.GE.': return LiteralNode(v1 >= v2)
                elif op == '.LE.': return LiteralNode(v1 <= v2)
                elif op == '.AND.': return LiteralNode(v1 and v2)
                elif op == '.OR.': return LiteralNode(v1 or v2)
            except Exception:
                pass # Se der erro (ex: divisão por zero), devolve a expressão original e a VM lida com isso

        # Se não deu para otimizar, devolve a expressão como estava (mas com os filhos possivelmente otimizados)
        return node
        
    def visit_UnaryOpNode(self, node):
        node.expr = self.visit(node.expr)
        if isinstance(node.expr, LiteralNode) and node.op.upper() == '.NOT.':
            return LiteralNode(not node.expr.value)
        return node

    # --- 2. DEAD CODE ELIMINATION ---
    def visit_IfNode(self, node):
        # 1. Otimiza a condição
        node.condition = self.visit(node.condition)
        # 2. Otimiza os blocos internos
        node.then_block = self.optimize_block(node.then_block)
        if node.else_block:
            node.else_block = self.optimize_block(node.else_block)

        # 3. Se a condição for um Literal, sabemos exatamente que bloco vai correr!
        if isinstance(node.condition, LiteralNode):
            if node.condition.value is True:
                # O IF é inútil, devolvemos só o código de dentro do THEN
                return node.then_block 
            elif node.condition.value is False:
                # A condição nunca acontece. Devolvemos só o ELSE (se existir), ou nada (lista vazia)
                return node.else_block if node.else_block else []

        return node