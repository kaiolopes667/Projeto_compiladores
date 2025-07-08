from parser import NodoAvancar, NodoGirarDireita, NodoDefinirCor, NodoCorDeFundo, NodoDefinirEspessura, NodoAtribuicao, NodoVar, NodoIrPara, NodoRepita, NodoRecuar, NodoGirarEsquerda, NodoLevantarCaneta, NodoAbaixarCaneta, NodoLimparTela, NodoEsperar, NodoEscrever, NodoSe

def gerar_codigo(ast, saida="saida.py"):
    linhas = [
        "import turtle",
        "t = turtle.Turtle()",
        "screen = turtle.Screen()"
    ]
    variaveis = {}
    def gerar_comando(comando, indent=0):
        prefix = '    ' * indent
        # Declaração de variável: inicializa com 0
        if isinstance(comando, NodoVar):
            variaveis[comando.nome] = 0
            linhas.append(f"{prefix}{comando.nome} = 0")
        # Atribuição de variável
        elif isinstance(comando, NodoAtribuicao):
            valor = comando.valor
            if isinstance(valor, str):
                linhas.append(f'{prefix}{comando.nome} = "{valor}"')
            elif isinstance(valor, bool):
                linhas.append(f'{prefix}{comando.nome} = {str(valor)}')
            else:
                linhas.append(f"{prefix}{comando.nome} = {gerar_expr(valor)}")
        # Comando avancar
        elif isinstance(comando, NodoAvancar):
            linhas.append(f"{prefix}t.forward({gerar_expr(comando.valor)})")
        # Comando girar_direita
        elif isinstance(comando, NodoGirarDireita):
            linhas.append(f"{prefix}t.right({gerar_expr(comando.valor)})")
        # Comando definir_cor
        elif isinstance(comando, NodoDefinirCor):
            linhas.append(f"{prefix}t.pencolor(\"{comando.cor}\")")
        # Comando cor_de_fundo
        elif isinstance(comando, NodoCorDeFundo):
            linhas.append(f"{prefix}screen.bgcolor(\"{comando.cor}\")")
        # Comando definir_espessura
        elif isinstance(comando, NodoDefinirEspessura):
            linhas.append(f"{prefix}t.pensize({gerar_expr(comando.espessura)})")
        # Comando ir_para
        elif isinstance(comando, NodoIrPara):
            linhas.append(f"{prefix}t.goto({comando.x}, {comando.y})")
        # Estrutura de repetição repita
        elif isinstance(comando, NodoRepita):
            linhas.append(f"{prefix}for _ in range({comando.vezes}):")
            for filho in comando.comandos:
                gerar_comando(filho, indent + 1)
        # Comando recuar
        elif isinstance(comando, NodoRecuar):
            linhas.append(f"{prefix}t.backward({gerar_expr(comando.valor)})")
        # Comando girar_esquerda
        elif isinstance(comando, NodoGirarEsquerda):
            linhas.append(f"{prefix}t.left({gerar_expr(comando.valor)})")
        # Comando levantar_caneta
        elif isinstance(comando, NodoLevantarCaneta):
            linhas.append(f"{prefix}t.penup()")
        # Comando abaixar_caneta
        elif isinstance(comando, NodoAbaixarCaneta):
            linhas.append(f"{prefix}t.pendown()")
        # Comando limpar_tela
        elif isinstance(comando, NodoLimparTela):
            linhas.append(f"{prefix}t.clear()")
        # Comando esperar
        elif isinstance(comando, NodoEsperar):
            linhas.append(f"{prefix}turtle.time.sleep({gerar_expr(comando.valor)})")
        # Comando escrever
        elif isinstance(comando, NodoEscrever):
            texto = comando.texto
            if texto in variaveis:
                linhas.append(f"{prefix}t.write({texto})")
            else:
                linhas.append(f'{prefix}t.write("{texto}")')
        elif isinstance(comando, NodoSe):
            cond = comando.condicao
            if isinstance(cond, bool):
                cond_str = str(cond)
            else:
                cond_str = cond
            linhas.append(f"{prefix}if {cond_str}:")
            for c in comando.bloco_entao:
                gerar_comando(c, indent + 1)
            if comando.bloco_senao:
                linhas.append(f"{prefix}else:")
                for c in comando.bloco_senao:
                    gerar_comando(c, indent + 1)
    def gerar_expr(expr):
        from parser import NodoBinOp
        if isinstance(expr, NodoBinOp):
            esq = gerar_expr(expr.esquerda)
            dir = gerar_expr(expr.direita)
            return f"({esq} {expr.op} {dir})"
        elif isinstance(expr, str):
            return expr
        else:
            return str(expr)
    for comando in ast.comandos:
        gerar_comando(comando)
    linhas.append("turtle.done()")
    with open(saida, "w") as f:
        f.write('\n'.join(linhas))
    print(f"Código Python gerado em {saida}")
