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
        if hasattr(node, '__dict__'):
            for key, value in node.__dict__.items():
                if isinstance(value, list):
                    setattr(node, key, self.optimize_block(value))
                elif isinstance(value, Node):
                    setattr(node, key, self.visit(value))
        return node

    def optimize_block(self, block):
        new_block = []
        for stmt in block:
            opt_stmt = self.visit(stmt)
            if isinstance(opt_stmt, list):
                new_block.extend(opt_stmt)
            elif opt_stmt is not None:
                new_block.append(opt_stmt)
        return new_block

    def visit_BinOpNode(self, node):
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)

        if isinstance(node.left, LiteralNode) and isinstance(node.right, LiteralNode):
            v1 = node.left.value
            v2 = node.right.value
            op = node.op.upper()

            try:
                if op == '+': return LiteralNode(v1 + v2)
                elif op == '-': return LiteralNode(v1 - v2)
                elif op == '*': return LiteralNode(v1 * v2)
                elif op == '/': 
                    if v2 == 0: return node
                    if isinstance(v1, int) and isinstance(v2, int):
                        return LiteralNode(int(v1 / v2)) 
                    else:
                        return LiteralNode(v1 / v2)
                elif op == '.EQ.': return LiteralNode(v1 == v2)
                elif op == '.NE.': return LiteralNode(v1 != v2)
                elif op == '.GT.': return LiteralNode(v1 > v2)
                elif op == '.LT.': return LiteralNode(v1 < v2)
                elif op == '.GE.': return LiteralNode(v1 >= v2)
                elif op == '.LE.': return LiteralNode(v1 <= v2)
                elif op == '.AND.': return LiteralNode(v1 and v2)
                elif op == '.OR.': return LiteralNode(v1 or v2)
            except Exception:
                pass 

        return node
        
    def visit_UnaryOpNode(self, node):
        node.expr = self.visit(node.expr)
        if isinstance(node.expr, LiteralNode) and node.op.upper() == '.NOT.':
            return LiteralNode(not node.expr.value)
        return node

    def visit_IfNode(self, node):
        node.condition = self.visit(node.condition)
        node.then_block = self.optimize_block(node.then_block)
        if getattr(node, 'else_block', None):
            node.else_block = self.optimize_block(node.else_block)

        # ⚠️ A SALVAÇÃO DO CÓDIGO: Se tiver Label (ex: 20 IF), não apaga!
        if getattr(node, 'label', None):
            return node

        if isinstance(node.condition, LiteralNode):
            if node.condition.value is True:
                return node.then_block 
            elif node.condition.value is False:
                return node.else_block if getattr(node, 'else_block', None) else []

        return node