import ply.lex as lex

tokens = (
    'INICIO', 'FIM',
    'AVANCAR', 'VOLTAR',
    'GIRAR_DIREITA', 'GIRAR_ESQUERDA',
    'LEVANTAR_CANETA', 'BAIXAR_CANETA',
    'NUMERO'
)

t_ignore = ' \t'

def t_INICIO(t): r'inicio'; return t
def t_FIM(t): r'fim'; return t
def t_AVANCAR(t): r'avancar'; return t
def t_VOLTAR(t): r'voltar'; return t
def t_GIRAR_DIREITA(t): r'girar_direita'; return t
def t_GIRAR_ESQUERDA(t): r'girar_esquerda'; return t
def t_LEVANTAR_CANETA(t): r'levantar_caneta'; return t
def t_BAIXAR_CANETA(t): r'baixar_caneta'; return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Erro léxico: caractere inválido '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
