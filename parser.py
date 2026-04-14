import ply.yacc as yacc
from lexer import tokens

precedence = (
    ('left', 'AND', 'OR'),
    ('right', 'NOT'), # NOT tem alta precedência
    ('left', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
)

# --- 1. ESTRUTURA GLOBAL (Programa Principal + Funções Extras) ---
def p_programa(p):
    '''programa : bloco_principal lista_subprogramas
                | bloco_principal'''
    print("\n🏆 COMPILAÇÃO BEM SUCEDIDA: Estrutura validada a 100%!")

def p_bloco_principal(p):
    '''bloco_principal : cabecalho declaracoes instrucoes END
                       | cabecalho instrucoes END'''
    pass

def p_lista_subprogramas(p):
    '''lista_subprogramas : lista_subprogramas subprograma
                          | subprograma'''
    pass

# Definição de Subprogramas (Para o Exemplo 5)
def p_subprograma(p):
    '''subprograma : INTEGER FUNCTION IDEN LPAREN lista_ids_simples RPAREN declaracoes instrucoes END
                   | REAL FUNCTION IDEN LPAREN lista_ids_simples RPAREN declaracoes instrucoes END
                   | SUBROUTINE IDEN LPAREN lista_ids_simples RPAREN declaracoes instrucoes END'''
    print(f"-> Subprograma (Função/Subrotina) detetado: {p[3]}")

def p_cabecalho(p):
    '''cabecalho : PROGRAM IDEN'''
    print(f"-> Programa Principal: {p[2]}")

# --- 2. DECLARAÇÕES E ARRAYS (Para o Exemplo 4) ---
def p_declaracoes(p):
    '''declaracoes : declaracoes declaracao
                   | declaracao'''
    pass

def p_declaracao(p):
    '''declaracao : INTEGER lista_ids
                  | REAL lista_ids
                  | LOGICAL lista_ids'''
    pass

def p_lista_ids(p):
    '''lista_ids : lista_ids COMMA IDEN
                 | lista_ids COMMA IDEN LPAREN INT RPAREN
                 | IDEN
                 | IDEN LPAREN INT RPAREN''' # Permite declarar arrays: NUMS(5)
    pass

def p_lista_ids_simples(p):
    '''lista_ids_simples : lista_ids_simples COMMA IDEN
                         | IDEN'''
    pass

# --- 3. INSTRUÇÕES ---
def p_instrucoes(p):
    '''instrucoes : instrucoes instrucao_com_label
                  | instrucao_com_label'''
    pass

def p_instrucao_com_label(p):
    '''instrucao_com_label : INT instrucao
                           | instrucao'''
    if len(p) == 3:
        print(f"-> Label de linha detetado: {p[1]}")

def p_instrucao_print(p):
    '''instrucao : PRINT MUL COMMA lista_print'''
    print("-> Instrução PRINT")

def p_lista_print(p):
    '''lista_print : lista_print COMMA elemento_print
                   | elemento_print'''
    pass

def p_elemento_print(p):
    '''elemento_print : STRING
                      | expr'''
    pass

def p_instrucao_read(p):
    '''instrucao : READ MUL COMMA lista_ids_simples
                 | READ MUL COMMA IDEN LPAREN expr RPAREN''' # Lê para array: READ *, NUMS(I)
    print("-> Instrução READ")

# Permite atribuir a variáveis normais E a arrays
def p_instrucao_assign(p):
    '''instrucao : IDEN ASSIGN expr
                 | IDEN LPAREN expr RPAREN ASSIGN expr'''
    pass

def p_instrucao_do(p):
    '''instrucao : DO INT IDEN ASSIGN expr COMMA expr'''
    print("-> Bloco DO iniciado")

def p_instrucao_continue(p):
    '''instrucao : CONTINUE'''
    print("-> Instrução CONTINUE")

def p_instrucao_if_then(p):
    '''instrucao : IF LPAREN expr RPAREN THEN instrucoes ENDIF'''
    print("-> Bloco IF-THEN-ENDIF")

def p_instrucao_if_else(p):
    '''instrucao : IF LPAREN expr RPAREN THEN instrucoes ELSE instrucoes ENDIF'''
    print("-> Bloco IF-THEN-ELSE-ENDIF")

def p_instrucao_goto(p):
    '''instrucao : GOTO INT'''
    pass

def p_instrucao_return(p):
    '''instrucao : RETURN'''
    print("-> Instrução RETURN detetada")

# --- 4. EXPRESSÕES MATEMÁTICAS E LÓGICAS ---
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
    pass

def p_expr_unary(p):
    '''expr : NOT expr'''
    pass

def p_expr_group(p):
    '''expr : LPAREN expr RPAREN'''
    pass

def p_expr_logico(p):
    '''expr : TRUE
            | FALSE'''
    pass

# Esta regra mágica serve para MOD(NUM, I) E para arrays NUMS(I)
def p_expr_funcao_ou_array(p):
    '''expr : IDEN LPAREN lista_expr RPAREN'''
    pass

def p_lista_expr(p):
    '''lista_expr : lista_expr COMMA expr
                  | expr'''
    pass

def p_expr_termo(p):
    '''expr : INT
            | REAL_NUM
            | IDEN'''
    pass

# --- 5. TRATAMENTO DE ERROS ---
def p_error(p):
    if p:
        print(f"❌ Erro de Sintaxe: Token inesperado '{p.value}' (Tipo: {p.type}) na linha {p.lineno}")
    else:
        print("❌ Erro de Sintaxe: Fim de ficheiro inesperado. Falta um END?")

parser = yacc.yacc()