from parser import parser, NodoAvancar, NodoGirarDireita, NodoDefinirCor, NodoCorDeFundo, NodoDefinirEspessura, NodoAtribuicao, NodoVar, NodoIrPara, NodoPrograma, NodoRepita, NodoRecuar, NodoGirarEsquerda, NodoLevantarCaneta, NodoAbaixarCaneta, NodoLimparTela, NodoEsperar, NodoEscrever
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
            if tipo_var == "inteiro":
                if not isinstance(valor, int):
                    raise Exception(f"Atribuição inválida: variável '{comando.nome}' é inteiro, mas recebeu '{valor}'.")
            elif tipo_var == "texto":
                if not isinstance(valor, str):
                    raise Exception(f"Atribuição inválida: variável '{comando.nome}' é texto, mas recebeu '{valor}'.")
        elif isinstance(comando, (NodoAvancar, NodoGirarDireita, NodoDefinirEspessura)):
            valor = comando.valor if hasattr(comando, 'valor') else comando.espessura
            if isinstance(valor, str):
                if valor not in tabela_simbolos:
                    raise Exception(f"Variável '{valor}' não declarada antes do uso.")
                if tabela_simbolos[valor] != "inteiro":
                    raise Exception(f"Comando '{type(comando).__name__}' espera inteiro, mas variável '{valor}' é do tipo '{tabela_simbolos[valor]}'.")
            elif not isinstance(valor, int):
                raise Exception(f"Comando '{type(comando).__name__}' espera valor inteiro, mas recebeu '{valor}'.")
        elif isinstance(comando, NodoIrPara):
            if not (isinstance(comando.x, int) and isinstance(comando.y, int)):
                raise Exception(f"Comando 'ir_para' espera dois inteiros literais, mas recebeu '{comando.x}' e '{comando.y}'.")
        elif isinstance(comando, NodoRepita):
            if not isinstance(comando.vezes, int):
                raise Exception(f"Estrutura 'repita' espera um número inteiro literal, não variável.")
            for filho in comando.comandos:
                analisar_semantica(NodoPrograma([filho]), tabela_simbolos)
        elif isinstance(comando, NodoDefinirCor):
            cor = comando.cor
            if not isinstance(cor, str):
                raise Exception(f"Comando 'definir_cor' espera texto, mas recebeu '{cor}'.")
        elif isinstance(comando, NodoCorDeFundo):
            cor = comando.cor
            if not isinstance(cor, str):
                raise Exception(f"Comando 'cor_de_fundo' espera texto, mas recebeu '{cor}'.")
        elif isinstance(comando, (NodoRecuar, NodoGirarEsquerda)):
            valor = comando.valor
            if isinstance(valor, str):
                if valor not in tabela_simbolos:
                    raise Exception(f"Variável '{valor}' não declarada antes do uso.")
                if tabela_simbolos[valor] != "inteiro":
                    raise Exception(f"Comando '{type(comando).__name__}' espera inteiro, mas variável '{valor}' é do tipo '{tabela_simbolos[valor]}'.")
            elif not isinstance(valor, int):
                raise Exception(f"Comando '{type(comando).__name__}' espera valor inteiro, mas recebeu '{valor}'.")
        elif isinstance(comando, (NodoLevantarCaneta, NodoAbaixarCaneta, NodoLimparTela)):
            pass
        elif isinstance(comando, NodoEsperar):
            valor = comando.valor
            if isinstance(valor, str):
                if valor not in tabela_simbolos:
                    raise Exception(f"Variável '{valor}' não declarada antes do uso.")
                if tabela_simbolos[valor] != "inteiro":
                    raise Exception(f"Comando 'esperar' espera inteiro, mas variável '{valor}' é do tipo '{tabela_simbolos[valor]}'.")
            elif not isinstance(valor, int):
                raise Exception(f"Comando 'esperar' espera valor inteiro, mas recebeu '{valor}'.")
        elif isinstance(comando, NodoEscrever):
            texto = comando.texto
            if not isinstance(texto, str):
                raise Exception(f"Comando 'escrever' espera texto, mas recebeu '{texto}'.")

if __name__ == "__main__":
    with open("entrada1.txt") as f:
        codigo = f.read()
    tokens = tokenize(codigo)
    ast = parser(tokens)
    analisar_semantica(ast)
