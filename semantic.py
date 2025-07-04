from parser import parser, NodoPrograma, NodoAvancar, NodoGirarDireita, NodoDefinirCor, NodoCorDeFundo, NodoDefinirEspessura, NodoAtribuicao, NodoVar, NodoIrPara, NodoRepita, NodoBinOp
from tokenizer import tokenize

def analisar_semantica(ast, tabela_simbolos=None):
    if tabela_simbolos is None:
        tabela_simbolos = {}
    for comando in ast.comandos:
        if isinstance(comando, NodoVar):
            if comando.nome in tabela_simbolos:
                raise Exception(f"Variável '{comando.nome}' já declarada.")
            if comando.tipo not in ["inteiro", "texto"]:
                raise Exception(f"Tipo '{comando.tipo}' não suportado para variável '{comando.nome}'.")
            tabela_simbolos[comando.nome] = comando.tipo
        elif isinstance(comando, NodoAtribuicao):
            if comando.nome not in tabela_simbolos:
                raise Exception(f"Variável '{comando.nome}' não declarada antes do uso.")
            tipo_var = tabela_simbolos[comando.nome]
            valor = comando.valor
            tipo_valor = tipo_expressao(valor, tabela_simbolos)
            if tipo_var != tipo_valor:
                raise Exception(f"Atribuição inválida: variável '{comando.nome}' é {tipo_var}, mas expressão é {tipo_valor}.")
        elif isinstance(comando, (NodoAvancar, NodoGirarDireita, NodoDefinirEspessura)):
            valor = comando.valor if hasattr(comando, 'valor') else comando.espessura
            tipo_valor = tipo_expressao(valor, tabela_simbolos)
            if tipo_valor != "inteiro":
                raise Exception(f"Comando '{type(comando).__name__}' espera inteiro, mas expressão é {tipo_valor}.")
        elif isinstance(comando, NodoIrPara):
            if not (isinstance(comando.x, int) and isinstance(comando.y, int)):
                raise Exception(f"Comando 'ir_para' espera dois inteiros literais, mas recebeu '{comando.x}' e '{comando.y}'.")
        elif isinstance(comando, NodoRepita):
            if not isinstance(comando.vezes, int):
                raise Exception(f"Estrutura 'repita' espera um número inteiro literal, não variável.")
            for filho in comando.comandos:
                analisar_semantica(NodoPrograma([filho]), tabela_simbolos.copy())
        elif isinstance(comando, NodoDefinirCor):
            cor = comando.cor
            if not isinstance(cor, str):
                raise Exception(f"Comando 'definir_cor' espera texto, mas recebeu '{cor}'.")
        elif isinstance(comando, NodoCorDeFundo):
            cor = comando.cor
            if not isinstance(cor, str):
                raise Exception(f"Comando 'cor_de_fundo' espera texto, mas recebeu '{cor}'.")
    print("Análise semântica OK")

def tipo_expressao(expr, tabela_simbolos):
    from parser import NodoBinOp
    if isinstance(expr, int):
        return "inteiro"
    if isinstance(expr, str):
        if expr in tabela_simbolos:
            return tabela_simbolos[expr]
        else:
            raise Exception(f"Variável '{expr}' não declarada antes do uso.")
    if isinstance(expr, NodoBinOp):
        tipo_esq = tipo_expressao(expr.esquerda, tabela_simbolos)
        tipo_dir = tipo_expressao(expr.direita, tabela_simbolos)
        if tipo_esq != "inteiro" or tipo_dir != "inteiro":
            raise Exception("Operações aritméticas só são permitidas entre inteiros.")
        return "inteiro"
    raise Exception("Expressão inválida para verificação de tipo.")

if __name__ == "__main__":
    with open("entrada1.txt") as f:
        codigo = f.read()
    tokens = tokenize(codigo)
    ast = parser(tokens)
    analisar_semantica(ast)
