

def validar_dados_categoria(dados):
    nome = dados.get("nome")

    if not nome:
        return {"erro": "nome obrigatorio"}, None

    categoria_validada = {
        "nome": nome
    }

    return None, categoria_validada