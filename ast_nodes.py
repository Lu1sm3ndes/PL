# ast_nodes.py

class Node:
    def __init__(self):
        self.label = None # Para suportar os labels das linhas do Fortran

    def __repr__(self):
        # Esta função faz com que a árvore seja legível quando fazemos print(ast)
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items() if k != 'label')
        label_str = f" [Label: {self.label}]" if self.label else ""
        return f"{self.__class__.__name__}({attrs}){label_str}"

class ProgramNode(Node):
    def __init__(self, name, body, subprograms=None, decls=None):
        super().__init__()
        self.name = name
        self.decls = decls or []
        self.body = body
        self.subprograms = subprograms or []

class VarDeclNode(Node):
    def __init__(self, type, name):
        super().__init__()
        self.type = type
        self.name = name

class AssignNode(Node):
    def __init__(self, var, expr):
        super().__init__()
        self.var = var
        self.expr = expr

class ArrayAssignNode(Node):
    def __init__(self, name, index, expr):
        super().__init__()
        self.name = name
        self.index = index
        self.expr = expr

class BinOpNode(Node):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

class UnaryOpNode(Node):
    def __init__(self, op, expr):
        super().__init__()
        self.op = op
        self.expr = expr

class LiteralNode(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

class VarNode(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name

class IfNode(Node):
    def __init__(self, condition, then_block, else_block=None):
        super().__init__()
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class DoNode(Node):
    def __init__(self, label_ref, var, start, end):
        super().__init__()
        self.label_ref = label_ref
        self.var = var
        self.start = start
        self.end = end

class ContinueNode(Node):
    def __init__(self):
        super().__init__()

class PrintNode(Node):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

class ReadNode(Node):
    def __init__(self, var, index=None):
        super().__init__()
        self.var = var
        self.index = index

class SubroutineNode(Node):
    def __init__(self, name, params, decls, body):
        super().__init__()
        self.name = name
        self.params = params
        self.decls = decls
        self.body = body

class CallNode(Node):
    def __init__(self, name, args):
        super().__init__()
        self.name = name
        self.args = args

class GotoNode(Node):
    def __init__(self, target):
        super().__init__()
        self.target = target

class ReturnNode(Node):
    def __init__(self):
        super().__init__()