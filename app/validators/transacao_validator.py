


def validar_dados_transacao(dados):
    categoria_id = dados.get("categoria_id")
    tipo = dados.get("tipo")
    valor = dados.get("valor")
    descricao = dados.get("descricao")

    if categoria_id is None:
        return{"erro":"categoria_id obrigatorio"}, None
    
    if not isinstance(categoria_id, int):
        return{"erro":"categoria_id deve ser um numero inteiro"}, None
    
    if categoria_id <= 0:
        return{"erro":"categoria_id deve ser maior que zero"}, None

    if tipo not in ["receita", "despesa"]:
        return{"erro": "tipo deve ser receita ou despesa"}, None

    if valor is None:
        return{"erro":"valor obrigatorio"}, None

    if valor <= 0:
        return{"erro":"valor deve ser maior que zero"}, None

    if not descricao:
        return{"erro":"descricao obrigatoria"}, None

    transacao_validada = {
        "categoria_id": categoria_id,
        "tipo": tipo,
        "valor": valor,
        "descricao": descricao
    }

    return None, transacao_validada
       