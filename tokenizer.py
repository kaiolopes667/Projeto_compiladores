import re

class Token:
    def __init__(self, tipo, valor, linha):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha
    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, linha={self.linha})"

PALAVRAS_CHAVE = {
    "inicio", "fim", "var", "inteiro", "texto", "real", "logico",
    "avancar", "recuar", "girar_direita", "girar_esquerda", "repita", "vezes", "se", "entao", "senao", "fim_se",
    "definir_cor", "cor_de_fundo", "definir_espessura", "ir_para", "fim_repita",
    "levantar_caneta", "abaixar_caneta", "limpar_tela", "esperar", "escrever"
}

OPERADORES = {
    '+': 'MAIS',
    '-': 'MENOS',
    '*': 'MULT',
    '/': 'DIV'
}

def tokenize(codigo):
    tokens = []
    linhas = codigo.split('\n')
    for num_linha, linha in enumerate(linhas, 1):
        linha = linha.split('//')[0]
        partes = re.findall(r'\w+|".*?"|\d+|[=;:+\-*/:]', linha)
        for parte in partes:
            if not parte.strip():
                continue  # ignora strings vazias
            if parte in PALAVRAS_CHAVE:
                tokens.append(Token("PALAVRA_CHAVE", parte, num_linha))
            elif parte in OPERADORES:
                tokens.append(Token(OPERADORES[parte], parte, num_linha))
            elif parte.isdigit():
                tokens.append(Token("NUMERO", int(parte), num_linha))
            elif parte.startswith('"') and parte.endswith('"'):
                tokens.append(Token("TEXTO", parte[1:-1], num_linha))
            elif parte == '=':
                tokens.append(Token("IGUAL", parte, num_linha))
            elif parte == ';':
                tokens.append(Token("PONTO_VIRGULA", parte, num_linha))
            elif parte == ':':
                tokens.append(Token("DOIS_PONTOS", parte, num_linha))
            elif re.match(r'^[a-zA-Z_]\w*$', parte):
                tokens.append(Token("IDENT", parte, num_linha))
            else:
                raise Exception(f"Token inválido '{parte}' na linha {num_linha}")
    return tokens

if __name__ == "__main__":
    with open("entrada1.txt") as f:
        codigo = f.read()
    tokens = tokenize(codigo)
    for t in tokens:
        print(t) 
