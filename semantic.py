def analisar_semantica(ast):
    tipo, comandos = ast
    for comando in comandos:
        nome, valor = comando
        if not isinstance(valor, int) or valor < 0:
            raise Exception(f"Erro semântico no comando '{nome}' com valor '{valor}'")
