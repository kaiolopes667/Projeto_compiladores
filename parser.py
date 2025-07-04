from tokenizer import tokenize, Token

class NodoPrograma:
    """Representa o programa inteiro (lista de comandos)"""
    def __init__(self, comandos):
        self.comandos = comandos
    def __repr__(self):
        return f"NodoPrograma({self.comandos})"

class NodoAvancar:
    """Comando avancar <valor>;"""
    def __init__(self, valor):
        self.valor = valor
    def __repr__(self):
        return f"NodoAvancar({self.valor})"

class NodoGirarDireita:
    """Comando girar_direita <valor>;"""
    def __init__(self, valor):
        self.valor = valor
    def __repr__(self):
        return f"NodoGirarDireita({self.valor})"

class NodoDefinirCor:
    """Comando definir_cor "cor";"""
    def __init__(self, cor):
        self.cor = cor
    def __repr__(self):
        return f"NodoDefinirCor({self.cor})"

class NodoCorDeFundo:
    """Comando cor_de_fundo "cor";"""
    def __init__(self, cor):
        self.cor = cor
    def __repr__(self):
        return f"NodoCorDeFundo({self.cor})"

class NodoDefinirEspessura:
    """Comando definir_espessura <valor>;"""
    def __init__(self, espessura):
        self.espessura = espessura
    def __repr__(self):
        return f"NodoDefinirEspessura({self.espessura})"

class NodoVar:
    """Declaração de variável: var <tipo>: <nome>;"""
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo
    def __repr__(self):
        return f"NodoVar({self.nome}, {self.tipo})"

class NodoAtribuicao:
    """Atribuição: <nome> = <expressao>;"""
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor
    def __repr__(self):
        return f"NodoAtribuicao({self.nome}, {self.valor})"

class NodoIrPara:
    """Comando ir_para <int> <int>;"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"NodoIrPara({self.x}, {self.y})"

class NodoRepita:
    """Estrutura de repetição: repita <num> vezes ... fim_repita;"""
    def __init__(self, vezes, comandos):
        self.vezes = vezes
        self.comandos = comandos
    def __repr__(self):
        return f"NodoRepita({self.vezes}, {self.comandos})"

class NodoBinOp:
    """Expressão binária: expr op expr (ex: lado + 5)"""
    def __init__(self, op, esquerda, direita):
        self.op = op
        self.esquerda = esquerda
        self.direita = direita
    def __repr__(self):
        return f"NodoBinOp({self.op}, {self.esquerda}, {self.direita})"


def parser(tokens):
    pos = 0  # posição atual na lista de tokens
    def consumir(tipo_esperado, valor_esperado=None):
        """Consome um token do tipo (e valor) esperado, ou lança erro sintático."""
        nonlocal pos
        if pos < len(tokens) and tokens[pos].tipo == tipo_esperado:
            if valor_esperado is None or tokens[pos].valor == valor_esperado:
                pos += 1
                return tokens[pos-1]
        esperado = valor_esperado if valor_esperado else tipo_esperado
        raise Exception(f"Esperado {esperado}, encontrado {tokens[pos].tipo} '{tokens[pos].valor}' na linha {tokens[pos].linha}")

    def parse_programa():
        """Reconhece o bloco principal: inicio ... fim"""
        comandos = []
        consumir("PALAVRA_CHAVE", "inicio")
        while tokens[pos].valor != "fim":
            comandos.append(parse_comando())
        consumir("PALAVRA_CHAVE", "fim")
        return NodoPrograma(comandos)

    def parse_comando():
        """Reconhece e constrói cada comando da linguagem"""
        if tokens[pos].valor == "avancar":
            consumir("PALAVRA_CHAVE", "avancar")
            valor = parse_expressao()
            consumir("PONTO_VIRGULA")
            return NodoAvancar(valor)
        elif tokens[pos].valor == "girar_direita":
            consumir("PALAVRA_CHAVE", "girar_direita")
            valor = parse_expressao()
            consumir("PONTO_VIRGULA")
            return NodoGirarDireita(valor)
        elif tokens[pos].valor == "definir_cor":
            consumir("PALAVRA_CHAVE", "definir_cor")
            cor = consumir("TEXTO")
            consumir("PONTO_VIRGULA")
            return NodoDefinirCor(cor.valor)
        elif tokens[pos].valor == "cor_de_fundo":
            consumir("PALAVRA_CHAVE", "cor_de_fundo")
            cor = consumir("TEXTO")
            consumir("PONTO_VIRGULA")
            return NodoCorDeFundo(cor.valor)
        elif tokens[pos].valor == "definir_espessura":
            consumir("PALAVRA_CHAVE", "definir_espessura")
            espessura = parse_expressao()
            consumir("PONTO_VIRGULA")
            return NodoDefinirEspessura(espessura)
        elif tokens[pos].valor == "ir_para":
            consumir("PALAVRA_CHAVE", "ir_para")
            x = consumir("NUMERO").valor
            y = consumir("NUMERO").valor
            consumir("PONTO_VIRGULA")
            return NodoIrPara(x, y)
        elif tokens[pos].valor == "repita":
            consumir("PALAVRA_CHAVE", "repita")
            vezes = consumir("NUMERO").valor
            consumir("PALAVRA_CHAVE", "vezes")
            comandos = []
            while tokens[pos].valor != "fim_repita":
                comandos.append(parse_comando())
            consumir("PALAVRA_CHAVE", "fim_repita")
            consumir("PONTO_VIRGULA") if pos < len(tokens) and tokens[pos].tipo == "PONTO_VIRGULA" else None
            return NodoRepita(vezes, comandos)
        elif tokens[pos].valor == "var":
            consumir("PALAVRA_CHAVE", "var")
            tipo = consumir("PALAVRA_CHAVE")
            consumir("DOIS_PONTOS") if pos < len(tokens) and tokens[pos].tipo == "DOIS_PONTOS" else None
            nome = consumir("IDENT")
            consumir("PONTO_VIRGULA") if pos < len(tokens) and tokens[pos].tipo == "PONTO_VIRGULA" else None
            return NodoVar(nome.valor, tipo.valor)
        elif tokens[pos].tipo == "IDENT":
            nome = consumir("IDENT")
            consumir("IGUAL")
            valor = parse_expressao()
            consumir("PONTO_VIRGULA")
            return NodoAtribuicao(nome.valor, valor)
        else:
            raise Exception(f"Comando desconhecido: {tokens[pos].valor} na linha {tokens[pos].linha}")

    def parse_expressao():
        node = parse_termo()
        while pos < len(tokens) and tokens[pos].tipo in ("MAIS", "MENOS"):
            op = tokens[pos].valor
            consumir(tokens[pos].tipo)
            direito = parse_termo()
            node = NodoBinOp(op, node, direito)
        return node

    def parse_termo():
        node = parse_fator()
        while pos < len(tokens) and tokens[pos].tipo in ("MULT", "DIV"):
            op = tokens[pos].valor
            consumir(tokens[pos].tipo)
            direito = parse_fator()
            node = NodoBinOp(op, node, direito)
        return node

    def parse_fator():
        if tokens[pos].tipo == "NUMERO":
            return consumir("NUMERO").valor
        elif tokens[pos].tipo == "IDENT":
            return consumir("IDENT").valor
        else:
            raise Exception(f"Valor inválido: {tokens[pos].valor} na linha {tokens[pos].linha}")

    return parse_programa()

if __name__ == "__main__":
    with open("entrada1.txt") as f:
        codigo = f.read()
    tokens = tokenize(codigo)
    ast = parser(tokens)
    print(ast)
