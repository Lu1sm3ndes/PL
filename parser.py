import ply.yacc as yacc
from lexer import tokens
from ast_nodes import * # Importa as classes que definimos para a árvore

precedence = (
    ('left', 'AND', 'OR'),
    ('right', 'NOT'),
    ('left', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
)

# --- 1. ESTRUTURA GLOBAL ---
def p_programa(p):
    '''programa : bloco_principal lista_subprogramas
                | bloco_principal'''
    if len(p) == 3:
        p[0] = ProgramNode(p[1].name, p[1].body, p[2])
    else:
        p[0] = p[1]
    print("\n🏆 AST CONSTRUÍDA: Estrutura pronta para análise semântica!")

def p_bloco_principal(p):
    '''bloco_principal : cabecalho declaracoes instrucoes END
                       | cabecalho instrucoes END'''
    if len(p) == 5:
        p[0] = ProgramNode(p[1], p[3], decls=p[2])
    else:
        p[0] = ProgramNode(p[1], p[2])

def p_lista_subprogramas(p):
    '''lista_subprogramas : lista_subprogramas subprograma
                          | subprograma'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_subprograma(p):
    '''subprograma : INTEGER FUNCTION IDEN LPAREN lista_ids_simples RPAREN declaracoes instrucoes END
                   | REAL FUNCTION IDEN LPAREN lista_ids_simples RPAREN declaracoes instrucoes END
                   | SUBROUTINE IDEN LPAREN lista_ids_simples RPAREN declaracoes instrucoes END'''
    # Se for FUNCTION p[1] é o tipo, se for SUBROUTINE p[1] é a keyword
    p[0] = SubroutineNode(p[3], p[5], p[7], p[8])

def p_cabecalho(p):
    '''cabecalho : PROGRAM IDEN'''
    p[0] = p[2]

# --- 2. DECLARAÇÕES ---
def p_declaracoes(p):
    '''declaracoes : declaracoes declaracao
                   | declaracao'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_declaracao(p):
    '''declaracao : INTEGER lista_ids
                  | REAL lista_ids
                  | LOGICAL lista_ids'''
    # Guarda o tipo e a lista de nomes/arrays
    p[0] = [VarDeclNode(p[1], var_name) for var_name in p[2]]

def p_lista_ids(p):
    '''lista_ids : lista_ids COMMA id_ou_array
                 | id_ou_array'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_id_ou_array(p):
    '''id_ou_array : IDEN
                   | IDEN LPAREN INT RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}[{p[3]}]"

def p_lista_ids_simples(p):
    '''lista_ids_simples : lista_ids_simples COMMA IDEN
                         | IDEN'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

# --- 3. INSTRUÇÕES ---
def p_instrucoes(p):
    '''instrucoes : instrucoes instrucao_com_label
                  | instrucao_com_label'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_instrucao_com_label(p):
    '''instrucao_com_label : INT instrucao
                           | instrucao'''
    if len(p) == 3:
        p[2].label = p[1] # Atribui o label ao objeto da instrução
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_instrucao_assign(p):
    '''instrucao : IDEN ASSIGN expr
                 | IDEN LPAREN expr RPAREN ASSIGN expr'''
    if len(p) == 4:
        p[0] = AssignNode(p[1], p[3])
    else:
        p[0] = ArrayAssignNode(p[1], p[3], p[6])

def p_instrucao_print(p):
    '''instrucao : PRINT MUL COMMA lista_print'''
    p[0] = PrintNode(p[4])

def p_lista_print(p):
    '''lista_print : lista_print COMMA elemento_print
                   | elemento_print'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_elemento_print(p):
    '''elemento_print : STRING
                      | expr'''
    p[0] = p[1]

def p_instrucao_read(p):
    '''instrucao : READ MUL COMMA IDEN
                 | READ MUL COMMA IDEN LPAREN expr RPAREN'''
    if len(p) == 5:
        p[0] = ReadNode(p[4])
    else:
        p[0] = ReadNode(p[4], p[6])

def p_instrucao_do(p):
    '''instrucao : DO INT IDEN ASSIGN expr COMMA expr'''
    # O corpo do ciclo será capturado na análise semântica pela label
    p[0] = DoNode(p[2], p[3], p[5], p[7])

def p_instrucao_continue(p):
    '''instrucao : CONTINUE'''
    p[0] = ContinueNode()

def p_instrucao_if(p):
    '''instrucao : IF LPAREN expr RPAREN THEN instrucoes ENDIF
                 | IF LPAREN expr RPAREN THEN instrucoes ELSE instrucoes ENDIF'''
    if len(p) == 8:
        p[0] = IfNode(p[3], p[6])
    else:
        p[0] = IfNode(p[3], p[6], p[8])

def p_instrucao_goto(p):
    '''instrucao : GOTO INT'''
    p[0] = GotoNode(p[2])

def p_instrucao_return(p):
    '''instrucao : RETURN'''
    p[0] = ReturnNode()

# --- 4. EXPRESSÕES ---

def p_expr_binop(p):
    '''expr : expr ADD expr
            | expr SUB expr
            | expr MUL expr
            | expr DIV expr
            | expr EQ expr
            | expr NE expr
            | expr LT expr
            | expr LE expr
            | expr GT expr
            | expr GE expr
            | expr AND expr
            | expr OR expr'''
    p[0] = BinOpNode(p[1], p[2], p[3])

def p_expr_unary(p):
    '''expr : NOT expr'''
    p[0] = UnaryOpNode(p[1], p[2])

def p_expr_group(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]

def p_expr_termo(p):
    '''expr : INT
            | REAL_NUM
            | IDEN'''
    if isinstance(p[1], (int, float)):
        p[0] = LiteralNode(p[1])
    else:
        p[0] = VarNode(p[1])

def p_expr_logico(p):
    '''expr : TRUE
            | FALSE'''
    # Transforma o '.TRUE.' do Fortran no True do Python (e vice-versa)
    if p[1].upper() == '.TRUE.':
        p[0] = LiteralNode(True)
    else:
        p[0] = LiteralNode(False)

def p_expr_funcao(p):
    '''expr : IDEN LPAREN lista_expr RPAREN'''
    p[0] = CallNode(p[1], p[3])

def p_lista_expr(p):
    '''lista_expr : lista_expr COMMA expr
                  | expr'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

# --- 5. ERRO ---
def p_error(p):
    if p:
        print(f"❌ Erro de Sintaxe: '{p.value}' na linha {p.lineno}")
    else:
        print("❌ Erro de Sintaxe: Fim de ficheiro inesperado.")

parser = yacc.yacc()