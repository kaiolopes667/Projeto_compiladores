import ply.yacc as yacc
from lexer import tokens

def p_programa(p):
    'programa : INICIO comandos FIM'
    p[0] = p[2]

def p_comandos(p):
    '''comandos : comandos comando
                | comando'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_comando_simples(p):
    '''comando : LEVANTAR_CANETA
               | BAIXAR_CANETA'''
    p[0] = (p[1],)

def p_comando_param(p):
    '''comando : AVANCAR NUMERO
               | VOLTAR NUMERO
               | GIRAR_DIREITA NUMERO
               | GIRAR_ESQUERDA NUMERO'''
    p[0] = (p[1], p[2])

def p_error(p):
    if p:
        print(f"Erro sintático na linha {p.lineno}: token '{p.value}'")
    else:
        print("Erro sintático no final do arquivo.")

parser = yacc.yacc()
