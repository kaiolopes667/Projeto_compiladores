def gerar_codigo(comandos, arquivo_saida="saida.py"):
    with open(arquivo_saida, "w") as f:
        f.write("import turtle\n")
        for cmd in comandos:
            instrucao = cmd[0]
            if instrucao == 'avancar':
                f.write(f"turtle.forward({cmd[1]})\n")
            elif instrucao == 'voltar':
                f.write(f"turtle.backward({cmd[1]})\n")
            elif instrucao == 'girar_direita':
                f.write(f"turtle.right({cmd[1]})\n")
            elif instrucao == 'girar_esquerda':
                f.write(f"turtle.left({cmd[1]})\n")
            elif instrucao == 'levantar_caneta':
                f.write("turtle.penup()\n")
            elif instrucao == 'baixar_caneta':
                f.write("turtle.pendown()\n")
        f.write("turtle.done()\n")
