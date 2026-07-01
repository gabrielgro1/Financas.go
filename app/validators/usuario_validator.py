

def validar_dados_usuario(dados):
    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not nome:
        return {"erro": "nome obrigatorio"}, None

    if not email:
        return {"erro": "email obrigatorio"}, None

    if "@" not in email:
        return {"erro": "email invalido"}, None

    if not senha:
        return {"erro": "senha obrigatoria"}, None

    if len(senha) < 6:
        return {"erro": "senha deve ter pelo menos 6 caracteres"}, None

    usuario_validado = {
        "nome": nome,
        "email": email,
        "senha": senha
    }

    return None, usuario_validado