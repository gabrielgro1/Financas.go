

def validar_dados_login(dados):
    email = dados.get("email")
    senha = dados.get("senha")

    if not email:
        return {"erro": "email obrigatorio"}, None

    if not senha:
        return {"erro": "senha obrigatoria"}, None

    return None, {
        "email": email,
        "senha": senha
    }