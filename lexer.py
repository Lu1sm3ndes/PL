import ply.lex as lex

# 1. Palavras do Fortran 77
reserved = {
    'PROGRAM': 'PROGRAM',
    'INTEGER': 'INTEGER',
    'REAL': 'REAL',
    'LOGICAL': 'LOGICAL',
    'IF': 'IF',
    'THEN': 'THEN',
    'ELSE': 'ELSE',
    'ENDIF': 'ENDIF',
    'DO': 'DO',
    'CONTINUE': 'CONTINUE',
    'GOTO': 'GOTO',
    'PRINT': 'PRINT',
    'READ': 'READ',
    'END': 'END',
    'SUBROUTINE': 'SUBROUTINE',
    'FUNCTION': 'FUNCTION',
    'RETURN': 'RETURN'
}

# 2. Tokens
tokens = [
    'INT', 'REAL_NUM', 'IDEN', 'STRING',
    'ADD', 'SUB', 'MUL', 'DIV', 'ASSIGN',
    'COMMA', 'LPAREN', 'RPAREN', 'COLON',
    'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
    'AND', 'OR', 'NOT', 'TRUE', 'FALSE'
] + list(reserved.values())

# 3. Expressões simples
t_ADD    = r'\+'
t_SUB    = r'-'
t_MUL    = r'\*'
t_DIV    = r'/'
t_ASSIGN = r'='
t_COMMA  = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON  = r':'

# Operadores relacionais e lógicos 
def t_EQ(t): r'\.EQ\.'; return t
def t_NE(t): r'\.NE\.'; return t
def t_LE(t): r'\.LE\.'; return t
def t_LT(t): r'\.LT\.'; return t
def t_GE(t): r'\.GE\.'; return t
def t_GT(t): r'\.GT\.'; return t
def t_AND(t): r'\.AND\.'; return t
def t_OR(t): r'\.OR\.'; return t
def t_NOT(t): r'\.NOT\.'; return t

# Booleanos
def t_TRUE(t): r'\.TRUE\.'; return t
def t_FALSE(t): r'\.FALSE\.'; return t

# 4. Strings
def t_STRING(t):
    r"'[^']*'"
    t.value = t.value[1:-1]
    return t

# 5. Números reais (floats, antes do int)
def t_REAL_NUM(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# 6. Identificadores e palavras reservadas
def t_IDEN(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value.upper(), 'IDEN') 
    return t

# 7. Números inteiros
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# 8. Comentários (Formato livre usa !)
def t_COMMENT(t):
    r'![^\n]*'
    pass # ignora o texto do comentário

# 9. Ignorar espaços e tabs
t_ignore = " \t"

# 10. Contar linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# 11. Tratamento de erros
def t_error(t):
    print(f"Símbolo inválido na linha {t.lexer.lineno}: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

def tokenize(data):
    lexer.lineno = 1 # Reinicia a contagem de linhas da nova análise
    lexer.input(data)
    return lexer