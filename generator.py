from parser import parser, NodoAvancar, NodoGirarDireita, NodoDefinirCor, NodoCorDeFundo, NodoDefinirEspessura, NodoAtribuicao, NodoVar, NodoIrPara, NodoRepita, NodoBinOp
from tokenizer import tokenize

def gerar_codigo(ast, saida="saida.py"):
    linhas = [
        "import turtle",
        "t = turtle.Turtle()",
        "screen = turtle.Screen()"
    ]
    variaveis = {}
    def gerar_expr(expr):
        if isinstance(expr, NodoBinOp):
            esq = gerar_expr(expr.esquerda)
            dir = gerar_expr(expr.direita)
            return f"({esq} {expr.op} {dir})"
        elif isinstance(expr, str):
            return expr
        else:
            return str(expr)
    def gerar_comando(comando, indent=0):
        prefix = '    ' * indent
        if isinstance(comando, NodoVar):
            variaveis[comando.nome] = 0
            linhas.append(f"{prefix}{comando.nome} = 0")
        elif isinstance(comando, NodoAtribuicao):
            variaveis[comando.nome] = comando.valor
            linhas.append(f"{prefix}{comando.nome} = {gerar_expr(comando.valor)}")
        elif isinstance(comando, NodoAvancar):
            linhas.append(f"{prefix}t.forward({gerar_expr(comando.valor)})")
        elif isinstance(comando, NodoGirarDireita):
            linhas.append(f"{prefix}t.right({gerar_expr(comando.valor)})")
        elif isinstance(comando, NodoDefinirCor):
            linhas.append(f"{prefix}t.pencolor(\"{comando.cor}\")")
        elif isinstance(comando, NodoCorDeFundo):
            linhas.append(f"{prefix}screen.bgcolor(\"{comando.cor}\")")
        elif isinstance(comando, NodoDefinirEspessura):
            linhas.append(f"{prefix}t.pensize({gerar_expr(comando.espessura)})")
        elif isinstance(comando, NodoIrPara):
            linhas.append(f"{prefix}t.goto({comando.x}, {comando.y})")
        elif isinstance(comando, NodoRepita):
            linhas.append(f"{prefix}for _ in range({comando.vezes}):")
            for filho in comando.comandos:
                gerar_comando(filho, indent + 1)
    for comando in ast.comandos:
        gerar_comando(comando)
    linhas.append("turtle.done()")
    with open(saida, "w") as f:
        f.write('\n'.join(linhas))
    print(f"Código Python gerado em {saida}")

if __name__ == "__main__":
    with open("entrada1.txt") as f:
        codigo = f.read()
    tokens = tokenize(codigo)
    ast = parser(tokens)
    gerar_codigo(ast)
