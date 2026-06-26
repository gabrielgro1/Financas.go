


def validar_dados_transacao(dados):
    tipo = dados.get("tipo")
    valor = dados.get("valor")
    descricao = dados.get("descricao")

    if tipo not in ["receita", "despesa"]:
        return {"erro": "tipo deve ser receita ou despesa"}, None

    if valor is None:
        return {"erro": "valor obrigatorio"}, None

    if valor <= 0:
        return {"erro": "valor deve ser maior que zero"}, None

    if not descricao:
        return {"erro": "descricao obrigatoria"}, None

    transacao_validada = {
        "tipo": tipo,
        "valor": valor,
        "descricao": descricao
    }

    return None, transacao_validada
       